import chromadb
from chromadb.config import Settings
import threading
from typing import Any, Dict

from app.core.env import get_env
import logging
logger = logging.getLogger("agents.utils.memory")

class ChromaDBManager:

    _instance = None
    _lock = threading.Lock()
    _collections: Dict[str, Any] = {}
    _client = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ChromaDBManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            try:
                from .chromadb_config import get_optimal_chromadb_client, is_windows_11
                import platform

                self._client = get_optimal_chromadb_client()

                system = platform.system()
                if system == "Windows":
                    if is_windows_11():
                        logger.info(f"📚 [ChromaDB] Windows 11优化配置初始化完成 (构建号: {platform.version()})")
                    else:
                        logger.info("📚 [ChromaDB] Windows 10兼容配置初始化完成")
                else:
                    logger.info(f"📚 [ChromaDB] {system}标准配置初始化完成")

                self._initialized = True
            except Exception as e:
                logger.error(f"❌ [ChromaDB] 初始化失败: {e}")
                try:
                    settings = Settings(
                        allow_reset=True,
                        anonymized_telemetry=False,
                        is_persistent=False
                    )
                    self._client = chromadb.Client(settings)
                    logger.info("📚 [ChromaDB] 使用备用配置初始化完成")
                except Exception as backup_error:
                    self._client = chromadb.Client()
                    logger.warning(f"⚠️ [ChromaDB] 使用最简配置初始化: {backup_error}")
                self._initialized = True

    def get_or_create_collection(self, name: str):
        with self._lock:
            if name in self._collections:
                logger.debug(f"📚 [ChromaDB] 使用缓存集合: {name}")
                return self._collections[name]

            try:
                collection = self._client.get_collection(name=name)
                logger.info(f"📚 [ChromaDB] 获取现有集合: {name}")
            except Exception as e:
                logger.debug(f"[ChromaDB] 获取集合失败，尝试创建: {e}")
                try:
                    collection = self._client.create_collection(name=name)
                    logger.info(f"📚 [ChromaDB] 创建新集合: {name}")
                except Exception as e:
                    try:
                        collection = self._client.get_collection(name=name)
                        logger.info(f"📚 [ChromaDB] 并发创建后获取集合: {name}")
                    except Exception as final_error:
                        logger.error(f"❌ [ChromaDB] 集合操作失败: {name}, 错误: {final_error}")
                        raise final_error

            self._collections[name] = collection
            return collection

class FinancialSituationMemory:
    def __init__(self, name, config):
        self.config = config
        self.llm_provider = config.get("llm_provider", "openai").lower()

        self.max_embedding_length = int(get_env('MAX_EMBEDDING_CONTENT_LENGTH', '50000'))
        self.enable_embedding_length_check = get_env('ENABLE_EMBEDDING_LENGTH_CHECK', 'true').lower() == 'true'

        from app.engine.agents.utils.embedding_resolver import resolve_embedding
        emb = resolve_embedding(self.llm_provider, config)

        self.client = emb.client
        self.embedding = emb.embedding_model
        self.fallback_available = emb.fallback_available
        self.fallback_client = emb.fallback_client
        self.fallback_embedding = emb.fallback_embedding

        self.chroma_manager = ChromaDBManager()
        self.situation_collection = self.chroma_manager.get_or_create_collection(name)

    def get_embedding(self, text):

        if self.client == "DISABLED":
            logger.debug("⚠️ 记忆功能已禁用，返回空向量")
            return [0.0] * 1024

        if not text or not isinstance(text, str):
            logger.warning("⚠️ 输入文本为空或无效，返回空向量")
            return [0.0] * 1024

        text_length = len(text)
        if text_length == 0:
            logger.warning("⚠️ 输入文本长度为0，返回空向量")
            return [0.0] * 1024
        
        if self.enable_embedding_length_check and text_length > self.max_embedding_length:
            logger.warning(f"⚠️ 文本过长({text_length:,}字符 > {self.max_embedding_length:,}字符)，跳过向量化")
            self._last_text_info = {
                'original_length': text_length,
                'processed_length': 0,
                'was_truncated': False,
                'was_skipped': True,
                'provider': self.llm_provider,
                'strategy': 'length_limit_skip',
                'max_length': self.max_embedding_length
            }
            return [0.0] * 1024
        
        if text_length > 8192:
            logger.info(f"📝 处理长文本: {text_length}字符，提供商: {self.llm_provider}")
        
        self._last_text_info = {
            'original_length': text_length,
            'processed_length': text_length,
            'was_truncated': False,
            'was_skipped': False,
            'provider': self.llm_provider,
            'strategy': 'no_truncation_with_fallback'
        }

        if (self.llm_provider == "dashscope" or
            self.llm_provider == "alibaba" or
            self.llm_provider == "qianfan" or
            (self.llm_provider == "google" and self.client is None) or
            (self.llm_provider == "deepseek" and self.client is None) or
            (self.llm_provider == "openrouter" and self.client is None)):
            try:
                import dashscope
                from dashscope import TextEmbedding

                if not hasattr(dashscope, 'api_key') or not dashscope.api_key:
                    logger.warning("⚠️ DashScope API密钥未设置，记忆功能降级")
                    return [0.0] * 1024

                response = TextEmbedding.call(
                    model=self.embedding,
                    input=text
                )

                if response.status_code == 200:
                    embedding = response.output['embeddings'][0]['embedding']
                    logger.debug(f"✅ DashScope embedding成功，维度: {len(embedding)}")
                    return embedding
                else:
                    error_msg = f"{response.code} - {response.message}"
                    
                    if any(keyword in error_msg.lower() for keyword in ['length', 'token', 'limit', 'exceed']):
                        logger.warning(f"⚠️ DashScope长度限制: {error_msg}")
                        
                        if hasattr(self, 'fallback_available') and self.fallback_available:
                            logger.info("💡 尝试使用OpenAI降级处理长文本")
                            try:
                                response = self.fallback_client.embeddings.create(
                                    model=self.fallback_embedding,
                                    input=text
                                )
                                embedding = response.data[0].embedding
                                logger.info(f"✅ OpenAI降级成功，维度: {len(embedding)}")
                                return embedding
                            except Exception as fallback_error:
                                logger.error(f"❌ OpenAI降级失败: {str(fallback_error)}")
                                logger.info("💡 所有降级选项失败，记忆功能降级")
                                return [0.0] * 1024
                        else:
                            logger.info("💡 无可用降级选项，记忆功能降级")
                            return [0.0] * 1024
                    else:
                        logger.error(f"❌ DashScope API错误: {error_msg}")
                        return [0.0] * 1024

            except Exception as e:
                error_str = str(e).lower()
                
                if any(keyword in error_str for keyword in ['length', 'token', 'limit', 'exceed', 'too long']):
                    logger.warning(f"⚠️ DashScope长度限制异常: {str(e)}")
                    
                    if hasattr(self, 'fallback_available') and self.fallback_available:
                        logger.info("💡 尝试使用OpenAI降级处理长文本")
                        try:
                            response = self.fallback_client.embeddings.create(
                                model=self.fallback_embedding,
                                input=text
                            )
                            embedding = response.data[0].embedding
                            logger.info(f"✅ OpenAI降级成功，维度: {len(embedding)}")
                            return embedding
                        except Exception as fallback_error:
                            logger.error(f"❌ OpenAI降级失败: {str(fallback_error)}")
                            logger.info("💡 所有降级选项失败，记忆功能降级")
                            return [0.0] * 1024
                    else:
                        logger.info("💡 无可用降级选项，记忆功能降级")
                        return [0.0] * 1024
                elif 'import' in error_str:
                    logger.error(f"❌ DashScope包未安装: {str(e)}")
                elif 'connection' in error_str:
                    logger.error(f"❌ DashScope网络连接错误: {str(e)}")
                elif 'timeout' in error_str:
                    logger.error(f"❌ DashScope请求超时: {str(e)}")
                else:
                    logger.error(f"❌ DashScope embedding异常: {str(e)}")
                
                logger.warning("⚠️ 记忆功能降级，返回空向量")
                return [0.0] * 1024
        else:
            if self.client is None:
                logger.warning("⚠️ 嵌入客户端未初始化，返回空向量")
                return [0.0] * 1024
            elif self.client == "DISABLED":
                logger.debug("⚠️ 内存功能已禁用，返回空向量")
                return [0.0] * 1024

            try:
                response = self.client.embeddings.create(
                    model=self.embedding,
                    input=text
                )
                embedding = response.data[0].embedding
                logger.debug(f"✅ {self.llm_provider} embedding成功，维度: {len(embedding)}")
                return embedding

            except Exception as e:
                error_str = str(e).lower()
                
                length_error_keywords = [
                    'token', 'length', 'too long', 'exceed', 'maximum', 'limit',
                    'context', 'input too large', 'request too large'
                ]
                
                is_length_error = any(keyword in error_str for keyword in length_error_keywords)
                
                if is_length_error:
                    logger.warning(f"⚠️ {self.llm_provider}长度限制: {str(e)}")
                    logger.info("💡 为保证分析准确性，不截断文本，记忆功能降级")
                else:
                    if 'attributeerror' in error_str:
                        logger.error(f"❌ {self.llm_provider} API调用错误: {str(e)}")
                    elif 'connectionerror' in error_str or 'connection' in error_str:
                        logger.error(f"❌ {self.llm_provider}网络连接错误: {str(e)}")
                    elif 'timeout' in error_str:
                        logger.error(f"❌ {self.llm_provider}请求超时: {str(e)}")
                    elif 'keyerror' in error_str:
                        logger.error(f"❌ {self.llm_provider}响应格式错误: {str(e)}")
                    else:
                        logger.error(f"❌ {self.llm_provider} embedding异常: {str(e)}")
                
                logger.warning("⚠️ 记忆功能降级，返回空向量")
                return [0.0] * 1024

    def get_embedding_config_status(self):
        return {
            'enabled': self.enable_embedding_length_check,
            'max_embedding_length': self.max_embedding_length,
            'max_embedding_length_formatted': f"{self.max_embedding_length:,}字符",
            'provider': self.llm_provider,
            'client_status': 'DISABLED' if self.client == "DISABLED" else 'ENABLED'
        }

    def get_last_text_info(self):
        return getattr(self, '_last_text_info', None)

    def add_situations(self, situations_and_advice):

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        
        query_embedding = self.get_embedding(current_situation)
        
        if all(x == 0.0 for x in query_embedding):
            logger.debug("⚠️ 查询embedding为空向量，返回空结果")
            return []
        
        collection_count = self.situation_collection.count()
        if collection_count == 0:
            logger.debug("📭 记忆库为空，返回空结果")
            return []
        
        actual_n_matches = min(n_matches, collection_count)
        
        try:
            results = self.situation_collection.query(
                query_embeddings=[query_embedding],
                n_results=actual_n_matches
            )
            
            memories = []
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]
                metadatas = results.get('metadatas', [[]])[0]
                distances = results.get('distances', [[]])[0]
                
                for i, doc in enumerate(documents):
                    metadata = metadatas[i] if i < len(metadatas) else {}
                    distance = distances[i] if i < len(distances) else 1.0
                    
                    memory_item = {
                        'situation': doc,
                        'recommendation': metadata.get('recommendation', ''),
                        'similarity': 1.0 - distance,
                        'distance': distance
                    }
                    memories.append(memory_item)
                
                if hasattr(self, '_last_text_info') and self._last_text_info.get('was_truncated'):
                    logger.info(f"🔍 截断文本查询完成，找到{len(memories)}个相关记忆")
                    logger.debug(f"📊 原文长度: {self._last_text_info['original_length']}, "
                               f"处理后长度: {self._last_text_info['processed_length']}")
                else:
                    logger.debug(f"🔍 记忆查询完成，找到{len(memories)}个相关记忆")
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ 记忆查询失败: {str(e)}")
            return []

    def get_cache_info(self):
        info = {
            'collection_count': self.situation_collection.count(),
            'client_status': 'enabled' if self.client != "DISABLED" else 'disabled',
            'embedding_model': self.embedding,
            'provider': self.llm_provider
        }
        
        if hasattr(self, '_last_text_info'):
            info['last_text_processing'] = self._last_text_info
            
        return info

async def fetch_memory_brief(memory, situation: str, n: int = 2) -> str:

    import asyncio

    if memory is None or not situation:
        return ""
    try:
        past = await asyncio.to_thread(memory.get_memories, situation, n_matches=n)
        if not past:
            return "暂无历史记忆数据可参考。"
        return "\n\n".join(rec.get("recommendation", "") for rec in past if rec.get("recommendation"))
    except Exception as e:
        logger.warning(f"⚠️ 历史记忆检索失败，跳过注入: {e}")
        return "暂无历史记忆数据可参考。"
