"""
⚡ Performance Optimizer Utility Component for Car Market Analysis Executive Dashboard

Advanced performance optimization system providing lazy loading, memory management,
caching strategies, and performance monitoring for optimal dashboard performance.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from datetime import datetime, timedelta
import time
import psutil
import gc
import threading
from functools import wraps, lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Import components
try:
    from src.business_logic import CarDataAnalyzer as analyzer
    from src.components.utils.data_manager import data_manager
    from src.components.utils.notification_system import notification_system
    from .status_indicators import status_indicators
except ImportError:
    analyzer = None
    data_manager = None
    notification_system = None
    status_indicators = None


class PerformanceMetric:
    """Performance metric tracking."""
    
    def __init__(self, name: str, value: float, unit: str = "", timestamp: datetime = None):
        """Initialize performance metric."""
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = timestamp or datetime.now()
        self.history: List[Tuple[datetime, float]] = []

    def update(self, value: float) -> None:
        """Update metric value."""
        self.history.append((self.timestamp, self.value))
        self.value = value
        self.timestamp = datetime.now()
        
        # Limit history size
        if len(self.history) > 1000:
            self.history = self.history[-1000:]

    def get_average(self, minutes: int = 5) -> float:
        """Get average value over specified minutes."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_values = [value for timestamp, value in self.history if timestamp >= cutoff_time]
        return np.mean(recent_values) if recent_values else self.value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat(),
            'history_length': len(self.history),
            'average_5min': self.get_average(5)
        }


class LazyLoader:
    """Lazy loading implementation for data and components."""
    
    def __init__(self, loader_function: Callable, cache_key: str = None, ttl_seconds: int = 300):
        """Initialize lazy loader."""
        self.loader_function = loader_function
        self.cache_key = cache_key or f"lazy_{hash(loader_function)}"
        self.ttl_seconds = ttl_seconds
        self._data = None
        self._last_load = None
        self._loading = False
        self._lock = threading.Lock()

    def load(self, force_reload: bool = False) -> Any:
        """Load data with caching."""
        with self._lock:
            # Check if data is already loaded and not expired
            if not force_reload and self._data is not None and self._last_load:
                if (datetime.now() - self._last_load).seconds < self.ttl_seconds:
                    return self._data
            
            # Check if already loading
            if self._loading:
                # Wait for loading to complete
                while self._loading:
                    time.sleep(0.1)
                return self._data
            
            # Start loading
            self._loading = True
            
            try:
                # Load data
                start_time = time.time()
                self._data = self.loader_function()
                self._last_load = datetime.now()
                
                load_time = time.time() - start_time
                if load_time > 1.0:  # Log slow loads
                    print(f"[PERF] Slow load detected: {self.cache_key} took {load_time:.2f}s")
                
                return self._data
                
            except Exception as e:
                print(f"[PERF] Error loading {self.cache_key}: {str(e)}")
                raise
            finally:
                self._loading = False

    def is_loaded(self) -> bool:
        """Check if data is loaded."""
        return self._data is not None

    def is_expired(self) -> bool:
        """Check if cached data is expired."""
        if not self._last_load:
            return True
        return (datetime.now() - self._last_load).seconds >= self.ttl_seconds

    def clear_cache(self) -> None:
        """Clear cached data."""
        with self._lock:
            self._data = None
            self._last_load = None


class MemoryManager:
    """Memory management and optimization."""
    
    def __init__(self, max_memory_mb: int = 500, cleanup_threshold: float = 0.8):
        """Initialize memory manager."""
        self.max_memory_mb = max_memory_mb
        self.cleanup_threshold = cleanup_threshold
        self.memory_history: List[Tuple[datetime, float]] = []
        self.large_objects: Dict[str, Any] = {}

    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage."""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / (1024 * 1024),  # Resident Set Size
            'vms_mb': memory_info.vms / (1024 * 1024),  # Virtual Memory Size
            'percent': process.memory_percent(),
            'available_mb': psutil.virtual_memory().available / (1024 * 1024)
        }

    def track_memory(self) -> None:
        """Track memory usage."""
        memory_usage = self.get_memory_usage()
        self.memory_history.append((datetime.now(), memory_usage['rss_mb']))
        
        # Limit history size
        if len(self.memory_history) > 1000:
            self.memory_history = self.memory_history[-1000:]

    def should_cleanup(self) -> bool:
        """Check if memory cleanup is needed."""
        memory_usage = self.get_memory_usage()
        return memory_usage['rss_mb'] > (self.max_memory_mb * self.cleanup_threshold)

    def perform_cleanup(self) -> Dict[str, Any]:
        """Perform memory cleanup."""
        cleanup_stats = {
            'before_mb': self.get_memory_usage()['rss_mb'],
            'objects_removed': 0,
            'cache_cleared': 0
        }
        
        # Clear large objects
        for key, obj in list(self.large_objects.items()):
            if hasattr(obj, 'clear_cache'):
                obj.clear_cache()
                cleanup_stats['cache_cleared'] += 1
            del self.large_objects[key]
            cleanup_stats['objects_removed'] += 1
        
        # Force garbage collection
        collected = gc.collect()
        cleanup_stats['gc_collected'] = collected
        
        cleanup_stats['after_mb'] = self.get_memory_usage()['rss_mb']
        cleanup_stats['memory_saved_mb'] = cleanup_stats['before_mb'] - cleanup_stats['after_mb']
        
        return cleanup_stats

    def register_large_object(self, key: str, obj: Any) -> None:
        """Register a large object for tracking."""
        self.large_objects[key] = obj

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        current_memory = self.get_memory_usage()
        
        if self.memory_history:
            memory_values = [memory for _, memory in self.memory_history]
            avg_memory = np.mean(memory_values)
            max_memory = max(memory_values)
            min_memory = min(memory_values)
        else:
            avg_memory = max_memory = min_memory = current_memory['rss_mb']
        
        return {
            'current_mb': current_memory['rss_mb'],
            'average_mb': avg_memory,
            'max_mb': max_memory,
            'min_mb': min_memory,
            'available_mb': current_memory['available_mb'],
            'percent_used': current_memory['percent'],
            'tracked_objects': len(self.large_objects),
            'history_length': len(self.memory_history)
        }


class PerformanceOptimizer:
    """
    ⚡ Executive-Grade Performance Optimizer
    
    Provides comprehensive performance optimization including lazy loading,
    memory management, caching strategies, and performance monitoring.
    """

    def __init__(self):
        """Initialize the PerformanceOptimizer."""
        self.analyzer = analyzer
        self.data_manager = data_manager
        self.notification_system = notification_system
        self.status_indicators = status_indicators
        
        # Performance tracking
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.performance_history: List[Dict[str, Any]] = []
        
        # Lazy loaders
        self.lazy_loaders: Dict[str, LazyLoader] = {}
        
        # Memory management
        self.memory_manager = MemoryManager()
        
        # Performance configuration
        self.config = {
            'enable_lazy_loading': True,
            'enable_memory_management': True,
            'enable_performance_monitoring': True,
            'cache_ttl_seconds': 300,
            'max_memory_mb': 500,
            'cleanup_threshold': 0.8,
            'performance_logging': True
        }
        
        # Initialize performance monitoring
        self._initialize_performance_monitoring()

    def _initialize_performance_monitoring(self) -> None:
        """Initialize performance monitoring."""
        # Initialize lazy loaders for common data
        if self.data_manager:
            self.add_lazy_loader(
                'sales_data',
                lambda: self.data_manager.load_sales_data(),
                ttl_seconds=600
            )
            
            self.add_lazy_loader(
                'price_data',
                lambda: self.data_manager.load_price_data(),
                ttl_seconds=600
            )
            
            self.add_lazy_loader(
                'market_share_data',
                lambda: self.data_manager.load_market_share_data(),
                ttl_seconds=900
            )
            
            self.add_lazy_loader(
                'basic_data',
                lambda: self.data_manager.load_basic_data(),
                ttl_seconds=1800
            )

    def add_lazy_loader(self, key: str, loader_function: Callable, ttl_seconds: int = None) -> None:
        """Add a lazy loader."""
        if ttl_seconds is None:
            ttl_seconds = self.config['cache_ttl_seconds']
        
        self.lazy_loaders[key] = LazyLoader(loader_function, key, ttl_seconds)
        
        # Register with memory manager
        self.memory_manager.register_large_object(key, self.lazy_loaders[key])

    def get_lazy_data(self, key: str, force_reload: bool = False) -> Any:
        """Get data using lazy loading."""
        if key in self.lazy_loaders:
            return self.lazy_loaders[key].load(force_reload)
        else:
            raise KeyError(f"Lazy loader '{key}' not found")

    def clear_lazy_cache(self, key: str = None) -> None:
        """Clear lazy loading cache."""
        if key:
            if key in self.lazy_loaders:
                self.lazy_loaders[key].clear_cache()
        else:
            for loader in self.lazy_loaders.values():
                loader.clear_cache()

    # ==================== PERFORMANCE MONITORING ====================

    def start_performance_tracking(self) -> None:
        """Start performance tracking."""
        if not self.config['enable_performance_monitoring']:
            return
        
        # Track memory usage
        if self.config['enable_memory_management']:
            self.memory_manager.track_memory()
        
        # Check for cleanup
        if self.memory_manager.should_cleanup():
            cleanup_stats = self.memory_manager.perform_cleanup()
            if self.notification_system:
                self.notification_system.info(
                    f"Memory cleanup: {cleanup_stats['memory_saved_mb']:.1f}MB saved"
                )

    def track_metric(self, name: str, value: float, unit: str = "") -> None:
        """Track a performance metric."""
        if name not in self.metrics:
            self.metrics[name] = PerformanceMetric(name, value, unit)
        else:
            self.metrics[name].update(value)

    def track_execution_time(self, name: str):
        """Decorator to track execution time."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self.track_metric(f"{name}_execution_time", execution_time, "seconds")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.track_metric(f"{name}_error_time", execution_time, "seconds")
                    raise
            return wrapper
        return decorator

    def measure_dataframe_operation(self, operation_name: str, df: pd.DataFrame, operation: Callable) -> pd.DataFrame:
        """Measure DataFrame operation performance."""
        start_time = time.time()
        start_memory = self.memory_manager.get_memory_usage()['rss_mb']
        
        try:
            result = operation(df)
            
            end_time = time.time()
            end_memory = self.memory_manager.get_memory_usage()['rss_mb']
            
            # Track metrics
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            self.track_metric(f"{operation_name}_time", execution_time, "seconds")
            self.track_metric(f"{operation_name}_memory_delta", memory_delta, "MB")
            self.track_metric(f"{operation_name}_rows", len(result), "rows")
            
            # Log slow operations
            if execution_time > 2.0:
                if self.notification_system:
                    self.notification_system.warning(
                        f"Slow operation detected: {operation_name} took {execution_time:.2f}s"
                    )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_metric(f"{operation_name}_error_time", execution_time, "seconds")
            raise

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {name: metric.to_dict() for name, metric in self.metrics.items()},
            'memory_stats': self.memory_manager.get_memory_stats(),
            'lazy_loader_stats': {}
        }
        
        # Lazy loader statistics
        for key, loader in self.lazy_loaders.items():
            summary['lazy_loader_stats'][key] = {
                'is_loaded': loader.is_loaded(),
                'is_expired': loader.is_expired(),
                'cache_key': loader.cache_key,
                'ttl_seconds': loader.ttl_seconds
            }
        
        return summary

    # ==================== OPTIMIZATION STRATEGIES ====================

    def optimize_dataframe(self, df: pd.DataFrame, name: str = "dataframe") -> pd.DataFrame:
        """Optimize DataFrame memory usage."""
        if df.empty:
            return df
        
        original_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        # Optimize numeric columns
        for col in df.select_dtypes(include=[np.number]).columns:
            col_min = df[col].min()
            col_max = df[col].max()
            
            if df[col].dtype == 'int64':
                if col_min >= 0:
                    if col_max < 255:
                        df[col] = df[col].astype('uint8')
                    elif col_max < 65535:
                        df[col] = df[col].astype('uint16')
                    else:
                        df[col] = df[col].astype('uint32')
                else:
                    if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype('int8')
                    elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype('int16')
                    else:
                        df[col] = df[col].astype('int32')
            
            elif df[col].dtype == 'float64':
                df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Optimize categorical columns
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # If less than 50% unique values
                df[col] = df[col].astype('category')
        
        optimized_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
        memory_reduction = original_memory - optimized_memory
        reduction_percent = (memory_reduction / original_memory * 100) if original_memory > 0 else 0
        
        # Track optimization
        self.track_metric(f"{name}_optimization_reduction_mb", memory_reduction, "MB")
        self.track_metric(f"{name}_optimization_reduction_percent", reduction_percent, "%")
        
        if reduction_percent > 10:  # Log significant optimizations
            if self.notification_system:
                self.notification_system.info(
                    f"DataFrame optimized: {name} - {reduction_percent:.1f}% memory reduction"
                )
        
        return df

    def parallel_data_processing(self, operations: List[Tuple[str, Callable, Any]], max_workers: int = 4) -> Dict[str, Any]:
        """Process multiple operations in parallel."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all operations
            future_to_name = {
                executor.submit(operation, data): name
                for name, operation, data in operations
            }
            
            # Collect results
            for future in as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    start_time = time.time()
                    result = future.result()
                    execution_time = time.time() - start_time
                    
                    results[name] = {
                        'data': result,
                        'execution_time': execution_time,
                        'success': True
                    }
                    
                    self.track_metric(f"parallel_{name}_time", execution_time, "seconds")
                    
                except Exception as e:
                    results[name] = {
                        'data': None,
                        'execution_time': 0,
                        'success': False,
                        'error': str(e)
                    }
        
        return results

    def batch_dataframe_operations(self, df: pd.DataFrame, operations: List[Callable], batch_size: int = 1000) -> List[pd.DataFrame]:
        """Perform batch operations on large DataFrames."""
        if len(df) <= batch_size:
            # Process entire DataFrame if small
            results = []
            for operation in operations:
                result = self.measure_dataframe_operation("batch_operation", df, operation)
                results.append(result)
            return results
        
        # Process in batches
        results = []
        num_batches = (len(df) + batch_size - 1) // batch_size
        
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(df))
            batch_df = df.iloc[start_idx:end_idx].copy()
            
            batch_results = []
            for operation in operations:
                result = self.measure_dataframe_operation(f"batch_{i}_operation", batch_df, operation)
                batch_results.append(result)
            
            results.append(batch_results)
            
            # Progress tracking
            progress = (i + 1) / num_batches * 100
            self.track_metric("batch_progress", progress, "%")
        
        # Combine results
        combined_results = []
        for operation_idx in range(len(operations)):
            combined_df = pd.concat([batch_results[operation_idx] for batch_results in results], ignore_index=True)
            combined_results.append(combined_df)
        
        return combined_results

    # ==================== STREAMLIT INTEGRATION ====================

    def render_performance_dashboard(self) -> None:
        """Render performance monitoring dashboard."""
        st.markdown("## ⚡ Performance Monitoring")
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        memory_stats = self.memory_manager.get_memory_stats()
        
        with col1:
            st.metric("Memory Usage", f"{memory_stats['current_mb']:.1f} MB")
        
        with col2:
            st.metric("Memory Peak", f"{memory_stats['max_mb']:.1f} MB")
        
        with col3:
            st.metric("Available Memory", f"{memory_stats['available_mb']:.1f} MB")
        
        with col4:
            st.metric("Tracked Objects", memory_stats['tracked_objects'])
        
        # Lazy loader status
        st.markdown("### Lazy Loader Status")
        
        loader_data = []
        for key, loader in self.lazy_loaders.items():
            loader_data.append({
                'Loader': key,
                'Loaded': loader.is_loaded(),
                'Expired': loader.is_expired(),
                'TTL (s)': loader.ttl_seconds
            })
        
        if loader_data:
            st.dataframe(pd.DataFrame(loader_data), use_container_width=True)
        
        # Performance actions
        st.markdown("### Performance Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Clear Cache"):
                self.clear_lazy_cache()
                st.success("Cache cleared successfully")
        
        with col2:
            if st.button("🗑️ Memory Cleanup"):
                cleanup_stats = self.memory_manager.perform_cleanup()
                st.success(f"Memory cleanup: {cleanup_stats['memory_saved_mb']:.1f}MB saved")
        
        with col3:
            if st.button("📊 Performance Report"):
                summary = self.get_performance_summary()
                st.json(summary)

    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        return {
            'config': self.config,
            'metrics_count': len(self.metrics),
            'lazy_loaders_count': len(self.lazy_loaders),
            'memory_stats': self.memory_manager.get_memory_stats(),
            'performance_summary': self.get_performance_summary()
        }


# Global instance for use throughout the application
performance_optimizer = PerformanceOptimizer()

