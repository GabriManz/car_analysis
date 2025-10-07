"""
🔔 Notification System Utility Component for Car Market Analysis Executive Dashboard

Advanced notification system providing alerts, warnings, success messages,
and system status notifications with different urgency levels and styling.
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import json
import time

# Import configuration
try:
    from src.components.config.app_config import COLOR_PALETTE
except ImportError:
    # Fallback configuration
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17a2b8'
    }


class NotificationType(Enum):
    """Notification type enumeration."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class NotificationPriority(Enum):
    """Notification priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Notification:
    """Individual notification class."""
    
    def __init__(self, message: str, notification_type: NotificationType = NotificationType.INFO,
                 priority: NotificationPriority = NotificationPriority.MEDIUM,
                 title: str = None, duration: int = 5, dismissible: bool = True,
                 actions: List[Dict[str, Any]] = None, metadata: Dict[str, Any] = None):
        """Initialize notification."""
        self.id = f"notif_{int(time.time() * 1000)}"
        self.message = message
        self.type = notification_type
        self.priority = priority
        self.title = title
        self.duration = duration  # Duration in seconds
        self.dismissible = dismissible
        self.actions = actions or []
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        self.expires_at = self.timestamp + timedelta(seconds=duration)
        self.is_read = False
        self.is_dismissed = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'message': self.message,
            'type': self.type.value,
            'priority': self.priority.value,
            'title': self.title,
            'duration': self.duration,
            'dismissible': self.dismissible,
            'actions': self.actions,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_read': self.is_read,
            'is_dismissed': self.is_dismissed
        }

    def is_expired(self) -> bool:
        """Check if notification has expired."""
        return datetime.now() > self.expires_at

    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.is_read = True

    def dismiss(self) -> None:
        """Dismiss notification."""
        self.is_dismissed = True


class NotificationSystem:
    """
    📢 Executive-Grade Notification System
    
    Provides comprehensive notification management with different types,
    priorities, persistence, and interactive features for the dashboard.
    """

    def __init__(self):
        """Initialize the NotificationSystem."""
        self.notifications: Dict[str, Notification] = {}
        self.notification_history: List[Notification] = []
        self.max_notifications = 50
        self.max_history = 200
        
        # Notification styling configuration
        self.styling_config = {
            NotificationType.INFO: {
                'color': COLOR_PALETTE['info'],
                'icon': 'ℹ️',
                'bg_color': f"{COLOR_PALETTE['info']}20",
                'border_color': COLOR_PALETTE['info']
            },
            NotificationType.SUCCESS: {
                'color': COLOR_PALETTE['success'],
                'icon': '✅',
                'bg_color': f"{COLOR_PALETTE['success']}20",
                'border_color': COLOR_PALETTE['success']
            },
            NotificationType.WARNING: {
                'color': COLOR_PALETTE['warning'],
                'icon': '⚠️',
                'bg_color': f"{COLOR_PALETTE['warning']}20",
                'border_color': COLOR_PALETTE['warning']
            },
            NotificationType.ERROR: {
                'color': COLOR_PALETTE['danger'],
                'icon': '❌',
                'bg_color': f"{COLOR_PALETTE['danger']}20",
                'border_color': COLOR_PALETTE['danger']
            },
            NotificationType.CRITICAL: {
                'color': COLOR_PALETTE['danger'],
                'icon': '🚨',
                'bg_color': f"{COLOR_PALETTE['danger']}30",
                'border_color': COLOR_PALETTE['danger']
            }
        }

    # ==================== NOTIFICATION CREATION METHODS ====================

    def create_notification(self, message: str, notification_type: NotificationType = NotificationType.INFO,
                          priority: NotificationPriority = NotificationPriority.MEDIUM,
                          title: str = None, duration: int = 5, dismissible: bool = True,
                          actions: List[Dict[str, Any]] = None, metadata: Dict[str, Any] = None) -> str:
        """Create a new notification."""
        notification = Notification(
            message=message,
            notification_type=notification_type,
            priority=priority,
            title=title,
            duration=duration,
            dismissible=dismissible,
            actions=actions,
            metadata=metadata
        )
        
        # Add to active notifications
        self.notifications[notification.id] = notification
        
        # Add to history
        self.notification_history.append(notification)
        
        # Cleanup old notifications
        self._cleanup_notifications()
        
        return notification.id

    def info(self, message: str, title: str = None, duration: int = 5, **kwargs) -> str:
        """Create an info notification."""
        return self.create_notification(
            message=message,
            notification_type=NotificationType.INFO,
            title=title,
            duration=duration,
            **kwargs
        )

    def success(self, message: str, title: str = None, duration: int = 5, **kwargs) -> str:
        """Create a success notification."""
        return self.create_notification(
            message=message,
            notification_type=NotificationType.SUCCESS,
            title=title,
            duration=duration,
            **kwargs
        )

    def warning(self, message: str, title: str = None, duration: int = 8, **kwargs) -> str:
        """Create a warning notification."""
        return self.create_notification(
            message=message,
            notification_type=NotificationType.WARNING,
            title=title,
            duration=duration,
            **kwargs
        )

    def error(self, message: str, title: str = None, duration: int = 10, **kwargs) -> str:
        """Create an error notification."""
        return self.create_notification(
            message=message,
            notification_type=NotificationType.ERROR,
            title=title,
            duration=duration,
            **kwargs
        )

    def critical(self, message: str, title: str = None, duration: int = 0, **kwargs) -> str:
        """Create a critical notification (non-dismissible by default)."""
        return self.create_notification(
            message=message,
            notification_type=NotificationType.CRITICAL,
            priority=NotificationPriority.URGENT,
            title=title,
            duration=duration,
            dismissible=False,
            **kwargs
        )

    # ==================== NOTIFICATION DISPLAY METHODS ====================

    def display_notifications(self, container=None, max_display: int = 5) -> None:
        """Display active notifications in the specified container."""
        if container is None:
            container = st
        
        # Get active notifications
        active_notifications = [n for n in self.notifications.values() if not n.is_dismissed and not n.is_expired()]
        
        # Sort by priority and timestamp
        priority_order = {
            NotificationPriority.URGENT: 0,
            NotificationPriority.HIGH: 1,
            NotificationPriority.MEDIUM: 2,
            NotificationPriority.LOW: 3
        }
        
        active_notifications.sort(
            key=lambda x: (priority_order.get(x.priority, 2), -x.timestamp.timestamp())
        )
        
        # Display notifications
        for notification in active_notifications[:max_display]:
            self._display_single_notification(notification, container)

    def _display_single_notification(self, notification: Notification, container) -> None:
        """Display a single notification."""
        styling = self.styling_config[notification.type]
        
        # Create notification HTML
        timestamp_str = notification.timestamp.strftime("%H:%M:%S")
        notification_html = f"""
dismiss_button = ""
        if notification.dismissible:
            dismiss_button = f\'<button onclick="dismissNotification(\'{notification.id}\')" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #666;">×</button>\'
        
        
        <div class="notification" style="
            background-color: {styling['bg_color']};
            border-left: 4px solid {styling['border_color']};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
        ">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="font-size: 20px; flex-shrink: 0;">
                    {styling['icon']}
                </div>
                <div style="flex: 1;">
                    {f"<h4 style='margin: 0 0 8px 0; color: {styling['color']};'>{notification.title}</h4>" if notification.title else ""}
                    <p style="margin: 0; color: #333; line-height: 1.4;">
                        {notification.message}
                    </p>
                    <div style="
                        font-size: 12px;
                        color: #666;
                        margin-top: 8px;
                    ">
                        {timestamp_str}
                    </div>
                </div>
                {dismiss_button}
            </div>
        </div>
        """
        
        container.markdown(notification_html, unsafe_allow_html=True)

    def display_notification_toast(self, notification: Notification, container=None) -> None:
        """Display notification as a toast message."""
        if container is None:
            container = st
        
        styling = self.styling_config[notification.type]
        
        if notification.type == NotificationType.SUCCESS:
            container.success(f"{styling['icon']} {notification.message}")
        elif notification.type == NotificationType.WARNING:
            container.warning(f"{styling['icon']} {notification.message}")
        elif notification.type in [NotificationType.ERROR, NotificationType.CRITICAL]:
            container.error(f"{styling['icon']} {notification.message}")
        else:
            container.info(f"{styling['icon']} {notification.message}")

    def display_notification_banner(self, notification: Notification, container=None) -> None:
        """Display notification as a banner."""
        if container is None:
            container = st
        
        styling = self.styling_config[notification.type]
        
        banner_html = f"""
        <div style="
            background-color: {styling['bg_color']};
            border: 1px solid {styling['border_color']};
            border-radius: 4px;
            padding: 12px;
            margin: 8px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="font-size: 16px;">{styling['icon']}</span>
            <span style="color: {styling['color']}; font-weight: 500;">
                {notification.title or notification.message}
            </span>
        </div>
        """
        
        container.markdown(banner_html, unsafe_allow_html=True)

    # ==================== NOTIFICATION MANAGEMENT METHODS ====================

    def dismiss_notification(self, notification_id: str) -> bool:
        """Dismiss a specific notification."""
        if notification_id in self.notifications:
            self.notifications[notification_id].dismiss()
            return True
        return False

    def mark_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        if notification_id in self.notifications:
            self.notifications[notification_id].mark_as_read()
            return True
        return False

    def clear_all_notifications(self) -> int:
        """Clear all active notifications."""
        count = len(self.notifications)
        for notification in self.notifications.values():
            notification.dismiss()
        return count

    def clear_notifications_by_type(self, notification_type: NotificationType) -> int:
        """Clear notifications of a specific type."""
        count = 0
        for notification in self.notifications.values():
            if notification.type == notification_type and not notification.is_dismissed:
                notification.dismiss()
                count += 1
        return count

    def get_active_notifications(self) -> List[Notification]:
        """Get list of active notifications."""
        return [n for n in self.notifications.values() if not n.is_dismissed and not n.is_expired()]

    def get_notifications_by_type(self, notification_type: NotificationType) -> List[Notification]:
        """Get notifications of a specific type."""
        return [n for n in self.notifications.values() if n.type == notification_type]

    def get_notifications_by_priority(self, priority: NotificationPriority) -> List[Notification]:
        """Get notifications of a specific priority."""
        return [n for n in self.notifications.values() if n.priority == priority]

    def get_unread_notifications(self) -> List[Notification]:
        """Get unread notifications."""
        return [n for n in self.notifications.values() if not n.is_read and not n.is_dismissed]

    # ==================== NOTIFICATION HISTORY METHODS ====================

    def get_notification_history(self, limit: int = 50) -> List[Notification]:
        """Get notification history."""
        return self.notification_history[-limit:]

    def clear_notification_history(self) -> int:
        """Clear notification history."""
        count = len(self.notification_history)
        self.notification_history.clear()
        return count

    def export_notification_history(self, format: str = 'json') -> str:
        """Export notification history."""
        history_data = [n.to_dict() for n in self.notification_history]
        
        if format.lower() == 'json':
            return json.dumps(history_data, indent=2, default=str)
        else:
            return str(history_data)

    # ==================== SYSTEM NOTIFICATION METHODS ====================

    def system_startup(self) -> str:
        """Create system startup notification."""
        return self.success(
            "System initialized successfully",
            title="System Startup",
            duration=3,
            metadata={'event': 'system_startup'}
        )

    def data_loaded(self, dataset_name: str, record_count: int) -> str:
        """Create data loaded notification."""
        return self.success(
            f"Loaded {record_count:,} records from {dataset_name}",
            title="Data Loaded",
            duration=4,
            metadata={'dataset': dataset_name, 'record_count': record_count}
        )

    def data_error(self, error_message: str, dataset_name: str = None) -> str:
        """Create data error notification."""
        title = f"Data Error - {dataset_name}" if dataset_name else "Data Error"
        return self.error(
            error_message,
            title=title,
            duration=10,
            metadata={'dataset': dataset_name, 'error': error_message}
        )

    def analysis_completed(self, analysis_type: str, duration_seconds: float) -> str:
        """Create analysis completed notification."""
        return self.success(
            f"{analysis_type} analysis completed in {duration_seconds:.1f} seconds",
            title="Analysis Complete",
            duration=5,
            metadata={'analysis_type': analysis_type, 'duration': duration_seconds}
        )

    def cache_updated(self, cache_key: str, cache_size_mb: float) -> str:
        """Create cache updated notification."""
        return self.info(
            f"Cache updated: {cache_key} ({cache_size_mb:.1f} MB)",
            title="Cache Updated",
            duration=3,
            metadata={'cache_key': cache_key, 'cache_size': cache_size_mb}
        )

    def performance_warning(self, metric: str, threshold: float, actual: float) -> str:
        """Create performance warning notification."""
        return self.warning(
            f"{metric} exceeds threshold: {actual:.1f} > {threshold:.1f}",
            title="Performance Warning",
            duration=8,
            metadata={'metric': metric, 'threshold': threshold, 'actual': actual}
        )

    def security_alert(self, alert_message: str, severity: str = "medium") -> str:
        """Create security alert notification."""
        priority = NotificationPriority.HIGH if severity == "high" else NotificationPriority.MEDIUM
        return self.critical(
            alert_message,
            title="Security Alert",
            duration=0,  # Critical alerts don't auto-dismiss
            priority=priority,
            metadata={'severity': severity, 'alert': alert_message}
        )

    # ==================== UTILITY METHODS ====================

    def _cleanup_notifications(self) -> None:
        """Clean up expired and old notifications."""
        # Remove expired notifications
        expired_ids = [nid for nid, notif in self.notifications.items() if notif.is_expired()]
        for nid in expired_ids:
            del self.notifications[nid]
        
        # Limit active notifications
        if len(self.notifications) > self.max_notifications:
            # Remove oldest notifications
            sorted_notifications = sorted(
                self.notifications.items(),
                key=lambda x: x[1].timestamp
            )
            excess_count = len(self.notifications) - self.max_notifications
            for nid, _ in sorted_notifications[:excess_count]:
                del self.notifications[nid]
        
        # Limit notification history
        if len(self.notification_history) > self.max_history:
            self.notification_history = self.notification_history[-self.max_history:]

    def get_notification_stats(self) -> Dict[str, Any]:
        """Get notification statistics."""
        active_notifications = self.get_active_notifications()
        unread_notifications = self.get_unread_notifications()
        
        # Count by type
        type_counts = {}
        for notification_type in NotificationType:
            type_counts[notification_type.value] = len(
                self.get_notifications_by_type(notification_type)
            )
        
        # Count by priority
        priority_counts = {}
        for priority in NotificationPriority:
            priority_counts[priority.value] = len(
                self.get_notifications_by_priority(priority)
            )
        
        return {
            'total_active': len(active_notifications),
            'total_unread': len(unread_notifications),
            'total_history': len(self.notification_history),
            'type_counts': type_counts,
            'priority_counts': priority_counts,
            'oldest_notification': min(
                (n.timestamp for n in active_notifications),
                default=None
            ),
            'newest_notification': max(
                (n.timestamp for n in active_notifications),
                default=None
            )
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get notification system status."""
        active_count = len(self.get_active_notifications())
        unread_count = len(self.get_unread_notifications())
        
        # Determine system status
        if unread_count > 10:
            status = "overloaded"
        elif unread_count > 5:
            status = "busy"
        elif active_count > 0:
            status = "active"
        else:
            status = "idle"
        
        return {
            'status': status,
            'active_notifications': active_count,
            'unread_notifications': unread_count,
            'history_size': len(self.notification_history),
            'max_notifications': self.max_notifications,
            'max_history': self.max_history
        }


# Global instance for use throughout the application
notification_system = NotificationSystem()

