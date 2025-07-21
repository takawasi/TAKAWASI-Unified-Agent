#!/usr/bin/env python3
"""
Memory Quantum Core - Persistent Intelligence System

Advanced memory system with quantum-like properties for persistent
cross-session intelligence and dynamic context management.

Integrated into TAKAWASI Unified Agent by: takawasi
License: Apache-2.0
"""

import asyncio
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import pickle

@dataclass
class MemoryQuantum:
    """Individual memory quantum with metadata"""
    id: str
    content: str
    content_type: str
    relevance_score: float
    access_count: int
    created_at: datetime
    last_accessed: datetime
    tags: List[str]
    relationships: List[str]
    context_hash: str
    importance_weight: float

class MemoryQuantumCore:
    """
    Memory Quantum Core System
    
    Features:
    - Persistent cross-session memory storage
    - Dynamic relevance scoring and context adaptation
    - Quantum-like superposition of memory states
    - Automatic memory consolidation and optimization
    - Cross-reference relationship mapping
    """
    
    def __init__(self, db_path: Optional[str] = None):
        print("🧠 Initializing Memory Quantum Core...")
        
        self.db_path = db_path or "memory_quantum_core.db"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Memory management settings
        self.max_memory_size = 10000  # Maximum number of quantums
        self.relevance_threshold = 0.3  # Minimum relevance to keep
        self.consolidation_interval = 100  # Quantums before consolidation
        
        # In-memory caches for performance
        self.quantum_cache = {}
        self.relationship_graph = {}
        self.access_patterns = {}
        
        # Performance metrics
        self.metrics = {
            'total_quantums': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'consolidations_performed': 0,
            'average_relevance': 0.0
        }
        
        self._initialize_database()
        self._load_existing_quantums()
        
        print("✅ Memory Quantum Core initialized")
    
    def _initialize_database(self):
        """Initialize SQLite database for quantum storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main quantums table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_quantums (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL,
                relevance_score REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                tags TEXT,  -- JSON array
                relationships TEXT,  -- JSON array
                context_hash TEXT NOT NULL,
                importance_weight REAL DEFAULT 1.0,
                quantum_data BLOB  -- Serialized quantum object
            )
        ''')
        
        # Relationships table for graph traversal
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quantum_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_quantum_id TEXT NOT NULL,
                target_quantum_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL DEFAULT 1.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_quantum_id) REFERENCES memory_quantums (id),
                FOREIGN KEY (target_quantum_id) REFERENCES memory_quantums (id)
            )
        ''')
        
        # Access patterns for optimization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantum_id TEXT NOT NULL,
                access_timestamp TEXT NOT NULL,
                access_context TEXT,
                session_id TEXT,
                FOREIGN KEY (quantum_id) REFERENCES memory_quantums (id)
            )
        ''')
        
        # System metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relevance ON memory_quantums(relevance_score DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_content_type ON memory_quantums(content_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_context_hash ON memory_quantums(context_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_source ON quantum_relationships(source_quantum_id)')
        
        conn.commit()
        conn.close()
        
        print("📊 Memory Quantum database initialized")
    
    def _load_existing_quantums(self):
        """Load existing quantums into memory cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM memory_quantums
        ''')
        total_count = cursor.fetchone()[0]
        
        # Load top quantums by relevance into cache
        cache_limit = min(1000, total_count)
        cursor.execute('''
            SELECT * FROM memory_quantums 
            ORDER BY relevance_score DESC, last_accessed DESC
            LIMIT ?
        ''', (cache_limit,))
        
        quantums = cursor.fetchall()
        
        for quantum_row in quantums:
            quantum = self._row_to_quantum(quantum_row)
            self.quantum_cache[quantum.id] = quantum
        
        conn.close()
        
        self.metrics['total_quantums'] = total_count
        print(f"📚 Loaded {len(self.quantum_cache)} quantums into cache (total: {total_count})")
    
    def _row_to_quantum(self, row: tuple) -> MemoryQuantum:
        """Convert database row to MemoryQuantum object"""
        return MemoryQuantum(
            id=row[0],
            content=row[1],
            content_type=row[2],
            relevance_score=row[3],
            access_count=row[4],
            created_at=datetime.fromisoformat(row[5]),
            last_accessed=datetime.fromisoformat(row[6]),
            tags=json.loads(row[7]) if row[7] else [],
            relationships=json.loads(row[8]) if row[8] else [],
            context_hash=row[9],
            importance_weight=row[10]
        )
    
    async def store_memory_quantum(self, content: str, content_type: str = "general", 
                                  tags: List[str] = None, context: Dict = None) -> str:
        """Store a new memory quantum"""
        # Generate unique ID
        content_hash = hashlib.md5(content.encode()).hexdigest()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        quantum_id = f"mq_{timestamp}_{content_hash[:8]}"
        
        # Generate context hash for grouping
        context_str = json.dumps(context or {}, sort_keys=True)
        context_hash = hashlib.md5(context_str.encode()).hexdigest()[:12]
        
        # Calculate initial relevance
        relevance_score = self._calculate_initial_relevance(content, content_type, tags)
        
        # Create quantum object
        quantum = MemoryQuantum(
            id=quantum_id,
            content=content,
            content_type=content_type,
            relevance_score=relevance_score,
            access_count=1,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            tags=tags or [],
            relationships=[],
            context_hash=context_hash,
            importance_weight=1.0
        )
        
        # Store in database
        await self._store_quantum_db(quantum)
        
        # Add to cache
        self.quantum_cache[quantum_id] = quantum
        
        # Update metrics
        self.metrics['total_quantums'] += 1
        
        # Check for consolidation
        if len(self.quantum_cache) > self.consolidation_interval:
            await self._consolidate_memory()
        
        print(f"💾 Stored quantum: {quantum_id} (relevance: {relevance_score:.3f})")
        return quantum_id
    
    async def search_memory_quantums(self, query: str, content_type: str = None, 
                                   limit: int = 10, relevance_threshold: float = None) -> List[Dict]:
        """Search memory quantums based on query"""
        print(f"🔍 Searching quantums: '{query}' (type: {content_type}, limit: {limit})")
        
        threshold = relevance_threshold or self.relevance_threshold
        search_results = []
        
        # Calculate query embedding/hash for similarity
        query_terms = set(query.lower().split())
        
        # Search in cache first
        cache_results = []
        for quantum_id, quantum in self.quantum_cache.items():
            if content_type and quantum.content_type != content_type:
                continue
                
            # Calculate similarity score
            similarity = self._calculate_similarity(query_terms, quantum)
            
            if similarity >= threshold:
                cache_results.append({
                    'quantum_id': quantum_id,
                    'content': quantum.content,
                    'content_type': quantum.content_type,
                    'relevance_score': quantum.relevance_score,
                    'similarity_score': similarity,
                    'tags': quantum.tags,
                    'last_accessed': quantum.last_accessed.isoformat(),
                    'access_count': quantum.access_count
                })
                
                # Update access patterns
                await self._record_access(quantum_id, query)
        
        # Sort by combined relevance and similarity
        cache_results.sort(
            key=lambda x: x['relevance_score'] * 0.6 + x['similarity_score'] * 0.4, 
            reverse=True
        )
        
        search_results.extend(cache_results[:limit])
        self.metrics['cache_hits'] += len(cache_results)
        
        # If not enough results, search database
        if len(search_results) < limit:
            db_results = await self._search_database(query, content_type, limit - len(search_results), threshold)
            search_results.extend(db_results)
            self.metrics['cache_misses'] += len(db_results)
        
        print(f"📊 Search complete: {len(search_results)} results found")
        return search_results[:limit]
    
    async def _search_database(self, query: str, content_type: str = None, 
                             limit: int = 10, threshold: float = 0.3) -> List[Dict]:
        """Search database for quantums not in cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build SQL query
        sql_parts = ['SELECT * FROM memory_quantums WHERE relevance_score >= ?']
        params = [threshold]
        
        if content_type:
            sql_parts.append('AND content_type = ?')
            params.append(content_type)
        
        # Simple text search (would be replaced with more sophisticated search)
        query_terms = query.lower().split()
        for term in query_terms[:3]:  # Limit to first 3 terms for performance
            sql_parts.append('AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)')
            like_term = f'%{term}%'
            params.extend([like_term, like_term])
        
        sql_parts.append('ORDER BY relevance_score DESC LIMIT ?')
        params.append(limit)
        
        sql_query = ' '.join(sql_parts)
        
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
        
        results = []
        query_terms_set = set(query.lower().split())
        
        for row in rows:
            quantum = self._row_to_quantum(row)
            
            # Skip if already in cache
            if quantum.id in self.quantum_cache:
                continue
            
            similarity = self._calculate_similarity(query_terms_set, quantum)
            
            results.append({
                'quantum_id': quantum.id,
                'content': quantum.content,
                'content_type': quantum.content_type,
                'relevance_score': quantum.relevance_score,
                'similarity_score': similarity,
                'tags': quantum.tags,
                'last_accessed': quantum.last_accessed.isoformat(),
                'access_count': quantum.access_count
            })
        
        conn.close()
        return results
    
    def _calculate_similarity(self, query_terms: set, quantum: MemoryQuantum) -> float:
        """Calculate similarity between query terms and quantum content"""
        content_terms = set(quantum.content.lower().split())
        tag_terms = set([tag.lower() for tag in quantum.tags])
        
        # Term overlap similarity
        content_overlap = len(query_terms.intersection(content_terms)) / max(len(query_terms), 1)
        tag_overlap = len(query_terms.intersection(tag_terms)) / max(len(query_terms), 1)
        
        # Access frequency bonus
        access_bonus = min(quantum.access_count / 10, 0.2)
        
        # Recency bonus
        days_since_access = (datetime.now() - quantum.last_accessed).days
        recency_bonus = max(0, 0.1 - days_since_access * 0.01)
        
        similarity = (content_overlap * 0.6 + tag_overlap * 0.3 + 
                     access_bonus + recency_bonus)
        
        return min(similarity, 1.0)
    
    def _calculate_initial_relevance(self, content: str, content_type: str, tags: List[str] = None) -> float:
        """Calculate initial relevance score for new quantum"""
        base_relevance = 0.5
        
        # Content length bonus (longer content tends to be more valuable)
        length_bonus = min(len(content) / 1000, 0.2)
        
        # Content type multipliers
        type_multipliers = {
            'task_result': 1.2,
            'error_log': 1.1,
            'success_pattern': 1.3,
            'user_preference': 1.4,
            'system_config': 1.1,
            'general': 1.0
        }
        
        type_multiplier = type_multipliers.get(content_type, 1.0)
        
        # Tag diversity bonus
        tag_bonus = min(len(tags or []) * 0.05, 0.15)
        
        relevance = (base_relevance + length_bonus + tag_bonus) * type_multiplier
        
        return min(relevance, 1.0)
    
    async def _store_quantum_db(self, quantum: MemoryQuantum):
        """Store quantum in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize quantum object
        quantum_blob = pickle.dumps(quantum)
        
        cursor.execute('''
            INSERT OR REPLACE INTO memory_quantums 
            (id, content, content_type, relevance_score, access_count, 
             created_at, last_accessed, tags, relationships, context_hash, 
             importance_weight, quantum_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            quantum.id,
            quantum.content,
            quantum.content_type,
            quantum.relevance_score,
            quantum.access_count,
            quantum.created_at.isoformat(),
            quantum.last_accessed.isoformat(),
            json.dumps(quantum.tags),
            json.dumps(quantum.relationships),
            quantum.context_hash,
            quantum.importance_weight,
            quantum_blob
        ))
        
        conn.commit()
        conn.close()
    
    async def _record_access(self, quantum_id: str, query_context: str):
        """Record quantum access for pattern analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO access_patterns 
            (quantum_id, access_timestamp, access_context, session_id)
            VALUES (?, ?, ?, ?)
        ''', (quantum_id, datetime.now().isoformat(), query_context, self.session_id))
        
        # Update quantum access count
        if quantum_id in self.quantum_cache:
            self.quantum_cache[quantum_id].access_count += 1
            self.quantum_cache[quantum_id].last_accessed = datetime.now()
            
            # Update database
            cursor.execute('''
                UPDATE memory_quantums 
                SET access_count = access_count + 1, last_accessed = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), quantum_id))
        
        conn.commit()
        conn.close()
    
    async def _consolidate_memory(self):
        """Consolidate memory by removing low-relevance quantums"""
        print("🔄 Starting memory consolidation...")
        
        if len(self.quantum_cache) <= self.max_memory_size:
            return
        
        # Sort quantums by combined score
        quantums_by_score = sorted(
            self.quantum_cache.items(),
            key=lambda x: (x[1].relevance_score * 0.6 + 
                          (x[1].access_count / 100) * 0.2 + 
                          (1 / max((datetime.now() - x[1].last_accessed).days, 1)) * 0.2),
            reverse=True
        )
        
        # Keep top quantums
        quantums_to_keep = quantums_by_score[:self.max_memory_size]
        quantums_to_remove = quantums_by_score[self.max_memory_size:]
        
        # Remove from cache
        for quantum_id, quantum in quantums_to_remove:
            if quantum.relevance_score < self.relevance_threshold:
                del self.quantum_cache[quantum_id]
                
                # Update relevance score in database (mark for potential deletion)
                await self._update_quantum_relevance(quantum_id, quantum.relevance_score * 0.8)
        
        self.metrics['consolidations_performed'] += 1
        print(f"✅ Consolidation complete: {len(quantums_to_remove)} quantums removed from cache")
    
    async def _update_quantum_relevance(self, quantum_id: str, new_relevance: float):
        """Update quantum relevance score in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE memory_quantums 
            SET relevance_score = ?
            WHERE id = ?
        ''', (new_relevance, quantum_id))
        
        conn.commit()
        conn.close()
    
    async def create_quantum_relationship(self, source_id: str, target_id: str, 
                                        relationship_type: str = "related", strength: float = 1.0):
        """Create relationship between two quantums"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO quantum_relationships
            (source_quantum_id, target_quantum_id, relationship_type, strength)
            VALUES (?, ?, ?, ?)
        ''', (source_id, target_id, relationship_type, strength))
        
        # Update quantum objects in cache
        if source_id in self.quantum_cache:
            if target_id not in self.quantum_cache[source_id].relationships:
                self.quantum_cache[source_id].relationships.append(target_id)
        
        if target_id in self.quantum_cache:
            if source_id not in self.quantum_cache[target_id].relationships:
                self.quantum_cache[target_id].relationships.append(source_id)
        
        conn.commit()
        conn.close()
        
        print(f"🔗 Created relationship: {source_id} -> {target_id} ({relationship_type})")
    
    async def get_related_quantums(self, quantum_id: str, relationship_types: List[str] = None) -> List[Dict]:
        """Get quantums related to a specific quantum"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = '''
            SELECT mq.*, qr.relationship_type, qr.strength
            FROM memory_quantums mq
            JOIN quantum_relationships qr ON (
                (qr.source_quantum_id = ? AND qr.target_quantum_id = mq.id) OR
                (qr.target_quantum_id = ? AND qr.source_quantum_id = mq.id)
            )
        '''
        params = [quantum_id, quantum_id]
        
        if relationship_types:
            placeholders = ','.join(['?' for _ in relationship_types])
            sql += f' WHERE qr.relationship_type IN ({placeholders})'
            params.extend(relationship_types)
        
        sql += ' ORDER BY qr.strength DESC, mq.relevance_score DESC'
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        related_quantums = []
        for row in results:
            quantum = self._row_to_quantum(row[:-2])  # Exclude relationship columns
            related_quantums.append({
                'quantum_id': quantum.id,
                'content': quantum.content,
                'content_type': quantum.content_type,
                'relevance_score': quantum.relevance_score,
                'relationship_type': row[-2],
                'relationship_strength': row[-1],
                'tags': quantum.tags
            })
        
        conn.close()
        return related_quantums
    
    def get_memory_stats(self) -> Dict:
        """Get memory system statistics"""
        stats = {
            'total_quantums': self.metrics['total_quantums'],
            'cached_quantums': len(self.quantum_cache),
            'cache_hit_rate': (self.metrics['cache_hits'] / 
                             max(self.metrics['cache_hits'] + self.metrics['cache_misses'], 1)),
            'consolidations_performed': self.metrics['consolidations_performed'],
            'session_id': self.session_id,
            'database_path': self.db_path,
            'memory_usage_estimate': len(self.quantum_cache) * 1024  # Rough estimate in bytes
        }
        
        # Calculate average relevance from cache
        if self.quantum_cache:
            avg_relevance = sum(q.relevance_score for q in self.quantum_cache.values()) / len(self.quantum_cache)
            stats['average_relevance'] = avg_relevance
        else:
            stats['average_relevance'] = 0.0
        
        return stats
    
    async def cleanup_low_relevance(self, threshold: float = 0.1):
        """Clean up quantums with very low relevance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find low relevance quantums
        cursor.execute('''
            SELECT id FROM memory_quantums 
            WHERE relevance_score < ? AND access_count < 2
        ''', (threshold,))
        
        low_relevance_ids = [row[0] for row in cursor.fetchall()]
        
        if low_relevance_ids:
            # Remove from database
            placeholders = ','.join(['?' for _ in low_relevance_ids])
            cursor.execute(f'DELETE FROM memory_quantums WHERE id IN ({placeholders})', low_relevance_ids)
            cursor.execute(f'DELETE FROM quantum_relationships WHERE source_quantum_id IN ({placeholders}) OR target_quantum_id IN ({placeholders})', low_relevance_ids * 2)
            cursor.execute(f'DELETE FROM access_patterns WHERE quantum_id IN ({placeholders})', low_relevance_ids)
            
            # Remove from cache
            for quantum_id in low_relevance_ids:
                if quantum_id in self.quantum_cache:
                    del self.quantum_cache[quantum_id]
            
            conn.commit()
            print(f"🗑️ Cleaned up {len(low_relevance_ids)} low-relevance quantums")
        
        conn.close()
        return len(low_relevance_ids)
    
    async def shutdown(self):
        """Gracefully shutdown memory system"""
        print("🔄 Shutting down Memory Quantum Core...")
        
        # Save final metrics
        final_stats = self.get_memory_stats()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for metric_name, metric_value in final_stats.items():
            if isinstance(metric_value, (int, float)):
                cursor.execute('''
                    INSERT INTO system_metrics (metric_name, metric_value, session_id)
                    VALUES (?, ?, ?)
                ''', (f"final_{metric_name}", metric_value, self.session_id))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Final stats: {final_stats['total_quantums']} total quantums, "
              f"{final_stats['cache_hit_rate']:.1%} cache hit rate")
        print(f"📊 Database preserved at: {self.db_path}")
        print("✅ Memory Quantum Core shutdown complete")

# Demo function
async def demo_memory_quantum():
    """Demonstrate Memory Quantum Core capabilities"""
    print("🎬 Memory Quantum Core Demo")
    print("=" * 50)
    
    memory = MemoryQuantumCore("demo_memory_quantum.db")
    
    # Store some sample quantums
    sample_data = [
        ("Task completed successfully: data analysis with 95% accuracy", "task_result", ["analysis", "success", "data"]),
        ("Error encountered: timeout in network request", "error_log", ["error", "network", "timeout"]),
        ("User prefers dark mode interface", "user_preference", ["ui", "preference", "dark_mode"]),
        ("System configuration updated for better performance", "system_config", ["config", "performance", "optimization"])
    ]
    
    quantum_ids = []
    for content, content_type, tags in sample_data:
        quantum_id = await memory.store_memory_quantum(content, content_type, tags)
        quantum_ids.append(quantum_id)
    
    # Create some relationships
    await memory.create_quantum_relationship(quantum_ids[0], quantum_ids[3], "improvement_related", 0.8)
    await memory.create_quantum_relationship(quantum_ids[1], quantum_ids[2], "user_impact", 0.6)
    
    # Search for quantums
    print("\n🔍 Search Tests:")
    
    search_queries = [
        "data analysis success",
        "network error timeout",
        "user interface preferences",
        "performance optimization"
    ]
    
    for query in search_queries:
        results = await memory.search_memory_quantums(query, limit=2)
        print(f"\nQuery: '{query}' -> {len(results)} results")
        for result in results:
            print(f"  - {result['content'][:60]}... (relevance: {result['relevance_score']:.3f})")
    
    # Get related quantums
    print(f"\n🔗 Related quantums to {quantum_ids[0]}:")
    related = await memory.get_related_quantums(quantum_ids[0])
    for rel in related:
        print(f"  - {rel['content'][:60]}... ({rel['relationship_type']})")
    
    # Show statistics
    print("\n📊 Memory Statistics:")
    stats = memory.get_memory_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    await memory.shutdown()

if __name__ == "__main__":
    # Install numpy if not available
    try:
        import numpy as np
    except ImportError:
        print("Note: numpy not available, using simplified calculations")
        # Create mock numpy
        class MockNumpy:
            @staticmethod
            def array(x):
                return x
        np = MockNumpy()
    
    asyncio.run(demo_memory_quantum())