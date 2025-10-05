"""
📤 Export Manager Utility Component for Car Market Analysis Executive Dashboard

Advanced export functionality providing multiple formats, scheduled exports,
custom report generation, and professional document creation.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
import json
import io
import base64
import zipfile
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import components
try:
    from ...business_logic import analyzer
    from .data_manager import data_manager
    from .notification_system import notification_system
except ImportError:
    analyzer = None
    data_manager = None
    notification_system = None


class ExportTemplate:
    """Export template configuration."""
    
    def __init__(self, template_id: str, name: str, description: str,
                 data_sources: List[str], format_options: List[str],
                 default_format: str = 'csv', metadata: Dict[str, Any] = None):
        """Initialize export template."""
        self.template_id = template_id
        self.name = name
        self.description = description
        self.data_sources = data_sources
        self.format_options = format_options
        self.default_format = default_format
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.usage_count = 0

    def increment_usage(self) -> None:
        """Increment usage count."""
        self.usage_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'template_id': self.template_id,
            'name': self.name,
            'description': self.description,
            'data_sources': self.data_sources,
            'format_options': self.format_options,
            'default_format': self.default_format,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'usage_count': self.usage_count
        }


class ExportManager:
    """
    📊 Executive-Grade Export Manager
    
    Provides comprehensive export functionality with multiple formats,
    custom templates, scheduled exports, and professional reporting.
    """

    def __init__(self):
        """Initialize the ExportManager."""
        self.analyzer = analyzer
        self.data_manager = data_manager
        self.notification_system = notification_system
        
        # Export templates
        self.templates: Dict[str, ExportTemplate] = {}
        self.export_history: List[Dict[str, Any]] = []
        self.scheduled_exports: List[Dict[str, Any]] = []
        
        # Initialize default templates
        self._initialize_default_templates()
        
        # Export configuration
        self.export_config = {
            'max_file_size_mb': 100,
            'max_records_per_export': 100000,
            'compression_enabled': True,
            'include_metadata': True,
            'default_timestamp_format': '%Y%m%d_%H%M%S'
        }

    def _initialize_default_templates(self) -> None:
        """Initialize default export templates."""
        
        # Executive Summary Template
        self.add_template(
            template_id="executive_summary",
            name="Executive Summary Report",
            description="Comprehensive executive summary with KPIs and insights",
            data_sources=["sales_data", "price_data", "market_share_data"],
            format_options=["xlsx", "pdf", "json"],
            default_format="xlsx"
        )
        
        # Market Analysis Template
        self.add_template(
            template_id="market_analysis",
            name="Market Analysis Report",
            description="Detailed market analysis and competitive intelligence",
            data_sources=["market_share_data", "price_data", "sales_data"],
            format_options=["xlsx", "csv", "json"],
            default_format="xlsx"
        )
        
        # Sales Performance Template
        self.add_template(
            template_id="sales_performance",
            name="Sales Performance Report",
            description="Sales trends, forecasting, and performance metrics",
            data_sources=["sales_data", "price_data"],
            format_options=["xlsx", "csv", "json"],
            default_format="xlsx"
        )
        
        # Data Quality Template
        self.add_template(
            template_id="data_quality",
            name="Data Quality Report",
            description="Data quality assessment and validation metrics",
            data_sources=["all_data"],
            format_options=["xlsx", "json"],
            default_format="xlsx"
        )
        
        # Custom Analysis Template
        self.add_template(
            template_id="custom_analysis",
            name="Custom Analysis Report",
            description="User-defined analysis with selected data and metrics",
            data_sources=["sales_data", "price_data", "market_share_data", "basic_data"],
            format_options=["xlsx", "csv", "json", "pdf"],
            default_format="xlsx"
        )

    def add_template(self, template_id: str, name: str, description: str,
                    data_sources: List[str], format_options: List[str],
                    default_format: str = 'csv', metadata: Dict[str, Any] = None) -> None:
        """Add a new export template."""
        template = ExportTemplate(
            template_id=template_id,
            name=name,
            description=description,
            data_sources=data_sources,
            format_options=format_options,
            default_format=default_format,
            metadata=metadata
        )
        
        self.templates[template_id] = template

    def get_template(self, template_id: str) -> Optional[ExportTemplate]:
        """Get export template by ID."""
        return self.templates.get(template_id)

    def list_templates(self) -> List[ExportTemplate]:
        """List all available templates."""
        return list(self.templates.values())

    def get_popular_templates(self, limit: int = 5) -> List[ExportTemplate]:
        """Get most popular templates."""
        return sorted(
            self.templates.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )[:limit]

    # ==================== DATA EXPORT METHODS ====================

    def export_data(self, template_id: str, format_type: str = None,
                   filters: Dict[str, Any] = None, include_metadata: bool = True) -> Dict[str, Any]:
        """Export data using specified template."""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' not found")
        
        # Use default format if not specified
        if format_type is None:
            format_type = template.default_format
        
        # Validate format
        if format_type not in template.format_options:
            raise ValueError(f"Format '{format_type}' not supported for template '{template_id}'")
        
        # Increment usage count
        template.increment_usage()
        
        # Prepare data
        export_data = self._prepare_export_data(template, filters)
        
        # Generate export
        result = self._generate_export(export_data, format_type, template, include_metadata)
        
        # Record export history
        self._record_export_history(template_id, format_type, result)
        
        return result

    def _prepare_export_data(self, template: ExportTemplate, filters: Dict[str, Any] = None) -> Dict[str, pd.DataFrame]:
        """Prepare data for export based on template."""
        export_data = {}
        
        for data_source in template.data_sources:
            if data_source == "sales_data":
                if self.data_manager:
                    export_data[data_source] = self.data_manager.load_sales_data()
                else:
                    export_data[data_source] = pd.DataFrame()
            
            elif data_source == "price_data":
                if self.data_manager:
                    export_data[data_source] = self.data_manager.load_price_data()
                else:
                    export_data[data_source] = pd.DataFrame()
            
            elif data_source == "market_share_data":
                if self.data_manager:
                    market_share = self.data_manager.load_data_with_cache(
                        'market_share_data',
                        lambda: self.analyzer.calculate_market_share() if self.analyzer else pd.DataFrame()
                    )
                    export_data[data_source] = market_share
                else:
                    export_data[data_source] = pd.DataFrame()
            
            elif data_source == "basic_data":
                if self.data_manager:
                    export_data[data_source] = self.data_manager.load_basic_data()
                else:
                    export_data[data_source] = pd.DataFrame()
            
            elif data_source == "all_data":
                # Export all available data
                all_data = self.data_manager.load_all_data() if self.data_manager else {}
                export_data.update(all_data)
        
        # Apply filters if provided
        if filters:
            export_data = self._apply_export_filters(export_data, filters)
        
        return export_data

    def _apply_export_filters(self, data: Dict[str, pd.DataFrame], filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """Apply filters to export data."""
        filtered_data = {}
        
        for source_name, df in data.items():
            if df.empty:
                filtered_data[source_name] = df
                continue
            
            filtered_df = df.copy()
            
            # Apply automaker filter
            if 'automakers' in filters and filters['automakers']:
                if 'Automaker' in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df['Automaker'].isin(filters['automakers'])]
            
            # Apply price range filter
            if 'price_range' in filters and filters['price_range']:
                min_price, max_price = filters['price_range']
                if 'price_mean' in filtered_df.columns:
                    filtered_df = filtered_df[
                        (filtered_df['price_mean'] >= min_price) & 
                        (filtered_df['price_mean'] <= max_price)
                    ]
            
            # Apply top N limit
            if 'top_n' in filters and filters['top_n']:
                if 'total_sales' in filtered_df.columns:
                    filtered_df = filtered_df.nlargest(filters['top_n'], 'total_sales')
            
            filtered_data[source_name] = filtered_df
        
        return filtered_data

    def _generate_export(self, data: Dict[str, pd.DataFrame], format_type: str,
                        template: ExportTemplate, include_metadata: bool) -> Dict[str, Any]:
        """Generate export in specified format."""
        timestamp = datetime.now().strftime(self.export_config['default_timestamp_format'])
        filename = f"{template.name.replace(' ', '_')}_{timestamp}"
        
        if format_type == 'csv':
            return self._export_to_csv(data, filename, template, include_metadata)
        
        elif format_type == 'xlsx':
            return self._export_to_xlsx(data, filename, template, include_metadata)
        
        elif format_type == 'json':
            return self._export_to_json(data, filename, template, include_metadata)
        
        elif format_type == 'pdf':
            return self._export_to_pdf(data, filename, template, include_metadata)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _export_to_csv(self, data: Dict[str, pd.DataFrame], filename: str,
                      template: ExportTemplate, include_metadata: bool) -> Dict[str, Any]:
        """Export data to CSV format."""
        csv_data = {}
        metadata = {}
        
        for source_name, df in data.items():
            if not df.empty:
                # Convert DataFrame to CSV string
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data[f"{source_name}.csv"] = csv_buffer.getvalue()
                
                # Add metadata
                if include_metadata:
                    metadata[source_name] = {
                        'rows': len(df),
                        'columns': len(df.columns),
                        'export_timestamp': datetime.now().isoformat(),
                        'template_id': template.template_id
                    }
        
        # Create ZIP file if multiple files
        if len(csv_data) > 1:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_name, content in csv_data.items():
                    zip_file.writestr(file_name, content)
                
                # Add metadata file
                if include_metadata:
                    zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            zip_buffer.seek(0)
            return {
                'content': zip_buffer.getvalue(),
                'filename': f"{filename}.zip",
                'mime_type': 'application/zip',
                'format': 'csv_zip',
                'file_count': len(csv_data),
                'metadata': metadata
            }
        
        # Single file export
        else:
            single_file_name = list(csv_data.keys())[0]
            single_file_content = csv_data[single_file_name]
            
            return {
                'content': single_file_content,
                'filename': f"{filename}.csv",
                'mime_type': 'text/csv',
                'format': 'csv',
                'file_count': 1,
                'metadata': metadata
            }

    def _export_to_xlsx(self, data: Dict[str, pd.DataFrame], filename: str,
                       template: ExportTemplate, include_metadata: bool) -> Dict[str, Any]:
        """Export data to Excel format."""
        try:
            # Create Excel writer
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Write each dataset to a separate sheet
                for source_name, df in data.items():
                    if not df.empty:
                        sheet_name = source_name.replace('_', ' ').title()[:31]  # Excel sheet name limit
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Add metadata sheet
                if include_metadata:
                    metadata_df = pd.DataFrame([
                        {
                            'Dataset': source_name,
                            'Rows': len(df),
                            'Columns': len(df.columns),
                            'Export_Timestamp': datetime.now().isoformat(),
                            'Template_ID': template.template_id
                        }
                        for source_name, df in data.items() if not df.empty
                    ])
                    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            excel_buffer.seek(0)
            
            return {
                'content': excel_buffer.getvalue(),
                'filename': f"{filename}.xlsx",
                'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'format': 'xlsx',
                'file_count': len([df for df in data.values() if not df.empty]),
                'metadata': {
                    'template_id': template.template_id,
                    'export_timestamp': datetime.now().isoformat(),
                    'sheets': list(data.keys())
                }
            }
            
        except ImportError:
            # Fallback to CSV if openpyxl not available
            if self.notification_system:
                self.notification_system.warning("Excel export requires openpyxl. Falling back to CSV.")
            return self._export_to_csv(data, filename, template, include_metadata)

    def _export_to_json(self, data: Dict[str, pd.DataFrame], filename: str,
                       template: ExportTemplate, include_metadata: bool) -> Dict[str, Any]:
        """Export data to JSON format."""
        json_data = {}
        metadata = {}
        
        for source_name, df in data.items():
            if not df.empty:
                # Convert DataFrame to JSON
                json_data[source_name] = {
                    'data': df.to_dict('records'),
                    'columns': list(df.columns),
                    'shape': df.shape
                }
                
                # Add metadata
                if include_metadata:
                    metadata[source_name] = {
                        'rows': len(df),
                        'columns': len(df.columns),
                        'export_timestamp': datetime.now().isoformat(),
                        'template_id': template.template_id
                    }
        
        # Combine data and metadata
        export_payload = {
            'export_info': {
                'template_id': template.template_id,
                'template_name': template.name,
                'export_timestamp': datetime.now().isoformat(),
                'format': 'json'
            },
            'data': json_data
        }
        
        if include_metadata:
            export_payload['metadata'] = metadata
        
        json_content = json.dumps(export_payload, indent=2, default=str)
        
        return {
            'content': json_content,
            'filename': f"{filename}.json",
            'mime_type': 'application/json',
            'format': 'json',
            'file_count': len(json_data),
            'metadata': metadata
        }

    def _export_to_pdf(self, data: Dict[str, pd.DataFrame], filename: str,
                      template: ExportTemplate, include_metadata: bool) -> Dict[str, Any]:
        """Export data to PDF format (placeholder)."""
        # PDF export would require additional libraries like reportlab
        # For now, return a placeholder
        if self.notification_system:
            self.notification_system.info("PDF export requires additional libraries. Use Excel or CSV instead.")
        
        return {
            'content': f"PDF export for {template.name} not yet implemented",
            'filename': f"{filename}.txt",
            'mime_type': 'text/plain',
            'format': 'pdf_placeholder',
            'file_count': 0,
            'metadata': {'note': 'PDF export not implemented'}
        }

    def _record_export_history(self, template_id: str, format_type: str, result: Dict[str, Any]) -> None:
        """Record export in history."""
        export_record = {
            'template_id': template_id,
            'format_type': format_type,
            'filename': result['filename'],
            'file_count': result['file_count'],
            'timestamp': datetime.now().isoformat(),
            'success': True
        }
        
        self.export_history.append(export_record)
        
        # Limit history size
        if len(self.export_history) > 100:
            self.export_history = self.export_history[-100:]

    # ==================== SCHEDULED EXPORTS ====================

    def schedule_export(self, template_id: str, schedule_config: Dict[str, Any]) -> str:
        """Schedule a recurring export."""
        schedule_id = f"schedule_{int(datetime.now().timestamp())}"
        
        schedule = {
            'schedule_id': schedule_id,
            'template_id': template_id,
            'format_type': schedule_config.get('format_type', 'xlsx'),
            'frequency': schedule_config.get('frequency', 'daily'),
            'time': schedule_config.get('time', '09:00'),
            'enabled': True,
            'created_at': datetime.now().isoformat(),
            'last_run': None,
            'next_run': self._calculate_next_run(schedule_config),
            'run_count': 0
        }
        
        self.scheduled_exports.append(schedule)
        
        if self.notification_system:
            self.notification_system.success(f"Export scheduled: {template_id} ({schedule['frequency']})")
        
        return schedule_id

    def _calculate_next_run(self, schedule_config: Dict[str, Any]) -> str:
        """Calculate next run time for scheduled export."""
        now = datetime.now()
        frequency = schedule_config.get('frequency', 'daily')
        time_str = schedule_config.get('time', '09:00')
        
        try:
            hour, minute = map(int, time_str.split(':'))
        except:
            hour, minute = 9, 0
        
        if frequency == 'daily':
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        
        elif frequency == 'weekly':
            # Next Monday at specified time
            days_ahead = 0 - now.weekday()  # Monday is 0
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        elif frequency == 'monthly':
            # First day of next month at specified time
            if now.month == 12:
                next_run = now.replace(year=now.year + 1, month=1, day=1, hour=hour, minute=minute, second=0, microsecond=0)
            else:
                next_run = now.replace(month=now.month + 1, day=1, hour=hour, minute=minute, second=0, microsecond=0)
        
        else:
            # Default to daily
            next_run = now + timedelta(days=1)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return next_run.isoformat()

    def get_scheduled_exports(self) -> List[Dict[str, Any]]:
        """Get all scheduled exports."""
        return self.scheduled_exports.copy()

    def cancel_scheduled_export(self, schedule_id: str) -> bool:
        """Cancel a scheduled export."""
        for i, schedule in enumerate(self.scheduled_exports):
            if schedule['schedule_id'] == schedule_id:
                self.scheduled_exports.pop(i)
                if self.notification_system:
                    self.notification_system.info(f"Scheduled export cancelled: {schedule_id}")
                return True
        return False

    # ==================== UTILITY METHODS ====================

    def get_export_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get export history."""
        return self.export_history[-limit:] if self.export_history else []

    def get_export_stats(self) -> Dict[str, Any]:
        """Get export statistics."""
        total_exports = len(self.export_history)
        successful_exports = len([e for e in self.export_history if e.get('success', False)])
        
        # Format usage
        format_usage = {}
        for export in self.export_history:
            format_type = export.get('format_type', 'unknown')
            format_usage[format_type] = format_usage.get(format_type, 0) + 1
        
        # Template usage
        template_usage = {}
        for template in self.templates.values():
            template_usage[template.template_id] = template.usage_count
        
        return {
            'total_exports': total_exports,
            'successful_exports': successful_exports,
            'success_rate': (successful_exports / total_exports * 100) if total_exports > 0 else 0,
            'format_usage': format_usage,
            'template_usage': template_usage,
            'scheduled_exports': len(self.scheduled_exports),
            'active_schedules': len([s for s in self.scheduled_exports if s.get('enabled', False)])
        }

    def render_export_interface(self) -> None:
        """Render export interface in Streamlit."""
        st.markdown("## 📤 Data Export Center")
        
        # Template selection
        templates = self.list_templates()
        template_options = {t.template_id: f"{t.name} - {t.description}" for t in templates}
        
        selected_template_id = st.selectbox(
            "Select Export Template",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x]
        )
        
        if selected_template_id:
            template = self.get_template(selected_template_id)
            
            # Format selection
            selected_format = st.selectbox(
                "Export Format",
                options=template.format_options,
                index=template.format_options.index(template.default_format)
            )
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                include_metadata = st.checkbox("Include Metadata", value=True)
            
            with col2:
                apply_filters = st.checkbox("Apply Current Filters", value=True)
            
            # Export button
            if st.button("🚀 Generate Export", type="primary"):
                try:
                    # Prepare filters
                    filters = {}
                    if apply_filters:
                        filters = st.session_state.get('app_filters', {})
                    
                    # Generate export
                    with st.spinner("Generating export..."):
                        result = self.export_data(
                            selected_template_id,
                            selected_format,
                            filters,
                            include_metadata
                        )
                    
                    # Download button
                    st.download_button(
                        label=f"📥 Download {result['filename']}",
                        data=result['content'],
                        file_name=result['filename'],
                        mime=result['mime_type']
                    )
                    
                    # Success notification
                    if self.notification_system:
                        self.notification_system.success(f"Export generated: {result['filename']}")
                    
                    # Show export info
                    st.success(f"Export generated successfully!")
                    st.info(f"Files: {result['file_count']}, Format: {result['format']}")
                    
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
                    if self.notification_system:
                        self.notification_system.error(f"Export failed: {str(e)}")

    def get_export_manager_status(self) -> Dict[str, Any]:
        """Get export manager status."""
        return {
            'templates_count': len(self.templates),
            'export_history_count': len(self.export_history),
            'scheduled_exports_count': len(self.scheduled_exports),
            'export_stats': self.get_export_stats(),
            'config': self.export_config
        }


# Global instance for use throughout the application
export_manager = ExportManager()

