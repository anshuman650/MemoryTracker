import psutil
import tracemalloc
import objgraph
import gc
from typing import Dict, Any

class MemoryUtils:
    @staticmethod
    def get_system_memory() -> Dict[str, Any]:
        """Get system-wide memory usage information"""
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free,
            "percent": memory.percent,
            "cached": memory.cached
        }
    
    @staticmethod
    def get_process_memory(pid: int) -> Dict[str, Any]:
        """Get memory information for a specific process"""
        try:
            process = psutil.Process(pid)
            mem_info = process.memory_info()
            return {
                "rss": mem_info.rss,  # Resident Set Size
                "vms": mem_info.vms,  # Virtual Memory Size
                "shared": mem_info.shared,
                "text": mem_info.text,
                "data": mem_info.data,
                "percent": process.memory_percent()
            }
        except psutil.NoSuchProcess:
            return {}
    
    @staticmethod
    def start_trace() -> None:
        """Start tracing memory allocations"""
        tracemalloc.start()
    
    @staticmethod
    def take_snapshot() -> Any:
        """Take a snapshot of current memory allocations"""
        return tracemalloc.take_snapshot()
    
    @staticmethod
    def compare_snapshots(snap1: Any, snap2: Any) -> Dict[str, Any]:
        """Compare two memory snapshots"""
        stats = snap2.compare_to(snap1, 'lineno')
        return {
            "total": sum(stat.size for stat in stats),
            "stats": stats
        }
    
    @staticmethod
    def get_top_objects(count: int = 10) -> Dict[str, int]:
        """Get top objects by count in memory"""
        gc.collect()  # Run garbage collection first
        objects = objgraph.most_common_types(limit=count)
        return dict(objects)
    
    @staticmethod
    def get_object_references(obj_type: str) -> Any:
        """Get reference graph for a specific object type"""
        return objgraph.by_type(obj_type)
