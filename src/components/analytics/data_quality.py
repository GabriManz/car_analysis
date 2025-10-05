"""
🔍 Data Quality Component for Car Market Analysis Executive Dashboard

Comprehensive data quality assessment and validation for automotive market data.
Provides quality metrics, validation reports, and data health indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Import configuration
try:
    from ..config.data_config import DATA_QUALITY_THRESHOLDS, VALIDATION_RULES
    from ..config.app_config import COLOR_PALETTE
except ImportError:
    # Fallback configuration
    DATA_QUALITY_THRESHOLDS = {
        'missing_data_warning': 0.05,
        'missing_data_error': 0.20,
        'duplicate_threshold': 0.02,
        'outlier_threshold': 0.05
    }
    VALIDATION_RULES = {}
    COLOR_PALETTE = {
        'primary': '#1f77b4',
        'secondary': '#0a9396',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e'
    }


class DataQuality:
    """
    🔬 Executive-Grade Data Quality Assessment
    
    Provides comprehensive data quality analysis, validation, and health monitoring
    for automotive market datasets with executive-grade reporting.
    """

    def __init__(self):
        """Initialize the DataQuality component with configuration."""
        self.quality_thresholds = DATA_QUALITY_THRESHOLDS
        self.validation_rules = VALIDATION_RULES
        self.color_palette = COLOR_PALETTE
        self.quality_reports = {}

    def assess_dataset_quality(self, data: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """Perform comprehensive quality assessment on a dataset."""
        if data.empty:
            return self._create_empty_quality_report()
        
        quality_report = {
            'dataset_name': dataset_name,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'basic_metrics': self._calculate_basic_metrics(data),
            'completeness': self._assess_completeness(data),
            'consistency': self._assess_consistency(data),
            'validity': self._assess_validity(data, dataset_name),
            'uniqueness': self._assess_uniqueness(data),
            'accuracy': self._assess_accuracy(data),
            'quality_score': 0,
            'quality_rating': '',
            'recommendations': []
        }
        
        # Calculate overall quality score
        quality_report['quality_score'] = self._calculate_overall_quality_score(quality_report)
        quality_report['quality_rating'] = self._get_quality_rating(quality_report['quality_score'])
        
        # Generate recommendations
        quality_report['recommendations'] = self._generate_quality_recommendations(quality_report)
        
        # Store report
        self.quality_reports[dataset_name] = quality_report
        
        return quality_report

    def _create_empty_quality_report(self) -> Dict[str, Any]:
        """Create a quality report for empty datasets."""
        return {
            'dataset_name': 'Unknown',
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'basic_metrics': {'rows': 0, 'columns': 0, 'memory_mb': 0},
            'completeness': {'score': 0, 'missing_data_ratio': 1.0},
            'consistency': {'score': 0, 'issues': []},
            'validity': {'score': 0, 'violations': []},
            'uniqueness': {'score': 0, 'duplicate_ratio': 1.0},
            'accuracy': {'score': 0, 'outlier_ratio': 1.0},
            'quality_score': 0,
            'quality_rating': 'Poor',
            'recommendations': ['Dataset is empty - check data source']
        }

    def _calculate_basic_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic dataset metrics."""
        return {
            'rows': len(data),
            'columns': len(data.columns),
            'memory_mb': data.memory_usage(deep=True).sum() / 1024**2,
            'dtypes': data.dtypes.to_dict(),
            'shape': data.shape
        }

    def _assess_completeness(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess data completeness (missing values)."""
        total_cells = len(data) * len(data.columns)
        missing_cells = data.isnull().sum().sum()
        missing_ratio = missing_cells / total_cells if total_cells > 0 else 0
        
        # Calculate completeness score (0-100)
        completeness_score = (1 - missing_ratio) * 100
        
        # Identify columns with high missing data
        column_missing_ratios = data.isnull().sum() / len(data)
        high_missing_columns = column_missing_ratios[column_missing_ratios > self.quality_thresholds['missing_data_warning']].to_dict()
        
        return {
            'score': completeness_score,
            'missing_data_ratio': missing_ratio,
            'total_missing_cells': int(missing_cells),
            'total_cells': total_cells,
            'high_missing_columns': high_missing_columns,
            'status': self._get_completeness_status(missing_ratio)
        }

    def _assess_consistency(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess data consistency (format, patterns, etc.)."""
        issues = []
        consistency_score = 100
        
        # Check for inconsistent data types in object columns
        for col in data.select_dtypes(include=['object']).columns:
            # Check for mixed data types
            unique_types = set(type(val).__name__ for val in data[col].dropna())
            if len(unique_types) > 1:
                issues.append(f"Column '{col}' has mixed data types: {unique_types}")
                consistency_score -= 10
            
            # Check for inconsistent formatting
            if col in ['Genmodel_ID', 'Automaker_ID']:
                # Check for consistent ID formatting
                if not data[col].str.match(r'^[A-Za-z0-9_-]+$', na=False).all():
                    issues.append(f"Column '{col}' has inconsistent ID formatting")
                    consistency_score -= 5
            
            # Check for inconsistent case in categorical data
            if col in ['Automaker', 'Genmodel']:
                case_issues = data[col].str.islower().sum() + data[col].str.isupper().sum()
                if case_issues > 0 and case_issues < len(data[col].dropna()):
                    issues.append(f"Column '{col}' has inconsistent case formatting")
                    consistency_score -= 5
        
        # Check for inconsistent date formats
        date_columns = [col for col in data.columns if 'year' in col.lower() or 'date' in col.lower()]
        for col in date_columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                # Check for reasonable year ranges
                if col.lower() == 'year':
                    min_year = data[col].min()
                    max_year = data[col].max()
                    if min_year < 1900 or max_year > 2030:
                        issues.append(f"Column '{col}' has unrealistic year values: {min_year}-{max_year}")
                        consistency_score -= 15
        
        return {
            'score': max(0, consistency_score),
            'issues': issues,
            'status': self._get_consistency_status(consistency_score)
        }

    def _assess_validity(self, data: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """Assess data validity against business rules."""
        violations = []
        validity_score = 100
        
        # Apply dataset-specific validation rules
        if dataset_name in self.validation_rules:
            rules = self.validation_rules[dataset_name]
            
            for column, rule in rules.items():
                if column in data.columns:
                    column_violations = self._validate_column_against_rules(data[column], column, rule)
                    violations.extend(column_violations)
                    validity_score -= len(column_violations) * 10
        
        # Apply general business rules
        general_violations = self._apply_general_validation_rules(data, dataset_name)
        violations.extend(general_violations)
        validity_score -= len(general_violations) * 5
        
        return {
            'score': max(0, validity_score),
            'violations': violations,
            'status': self._get_validity_status(validity_score)
        }

    def _assess_uniqueness(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess data uniqueness (duplicates)."""
        duplicate_rows = data.duplicated().sum()
        duplicate_ratio = duplicate_rows / len(data) if len(data) > 0 else 0
        
        # Calculate uniqueness score (0-100)
        uniqueness_score = (1 - duplicate_ratio) * 100
        
        # Check for key column uniqueness
        key_columns = ['Genmodel_ID', 'Automaker_ID']
        key_violations = []
        
        for col in key_columns:
            if col in data.columns:
                unique_count = data[col].nunique()
                total_count = len(data)
                if unique_count != total_count:
                    key_violations.append(f"Column '{col}' should be unique but has {total_count - unique_count} duplicates")
                    uniqueness_score -= 20
        
        return {
            'score': max(0, uniqueness_score),
            'duplicate_ratio': duplicate_ratio,
            'duplicate_rows': int(duplicate_rows),
            'key_violations': key_violations,
            'status': self._get_uniqueness_status(duplicate_ratio)
        }

    def _assess_accuracy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess data accuracy (outliers, reasonable values)."""
        accuracy_score = 100
        outliers = []
        
        # Check numeric columns for outliers
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in data.columns and data[col].notna().sum() > 0:
                # Use IQR method for outlier detection
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_count = ((data[col] < lower_bound) | (data[col] > upper_bound)).sum()
                outlier_ratio = outlier_count / len(data[col].dropna()) if len(data[col].dropna()) > 0 else 0
                
                if outlier_ratio > self.quality_thresholds['outlier_threshold']:
                    outliers.append(f"Column '{col}' has {outlier_count} outliers ({outlier_ratio:.1%})")
                    accuracy_score -= min(20, outlier_ratio * 100)
                
                # Business-specific accuracy checks
                if col == 'Entry_price' or col == 'Price':
                    # Check for reasonable price values
                    if (data[col] < 0).any():
                        outliers.append(f"Column '{col}' has negative prices")
                        accuracy_score -= 15
                    if (data[col] > 1000000).any():
                        outliers.append(f"Column '{col}' has unrealistic high prices")
                        accuracy_score -= 10
                
                elif 'year' in col.lower():
                    # Check for reasonable year values
                    if (data[col] < 1900).any() or (data[col] > 2030).any():
                        outliers.append(f"Column '{col}' has unrealistic year values")
                        accuracy_score -= 15
        
        return {
            'score': max(0, accuracy_score),
            'outliers': outliers,
            'status': self._get_accuracy_status(accuracy_score)
        }

    def _validate_column_against_rules(self, series: pd.Series, column_name: str, rules: Dict[str, Any]) -> List[str]:
        """Validate a column against specific rules."""
        violations = []
        
        # Required validation
        if rules.get('required', False):
            null_count = series.isnull().sum()
            if null_count > 0:
                violations.append(f"Column '{column_name}' is required but has {null_count} null values")
        
        # Type validation
        if 'type' in rules:
            expected_type = rules['type']
            if expected_type == 'string' and not pd.api.types.is_string_dtype(series):
                violations.append(f"Column '{column_name}' should be string type")
            elif expected_type == 'int' and not pd.api.types.is_integer_dtype(series):
                violations.append(f"Column '{column_name}' should be integer type")
        
        # Range validation
        if 'min' in rules or 'max' in rules:
            if pd.api.types.is_numeric_dtype(series):
                min_val = rules.get('min')
                max_val = rules.get('max')
                
                if min_val is not None and series.min() < min_val:
                    violations.append(f"Column '{column_name}' has values below minimum {min_val}")
                
                if max_val is not None and series.max() > max_val:
                    violations.append(f"Column '{column_name}' has values above maximum {max_val}")
        
        return violations

    def _apply_general_validation_rules(self, data: pd.DataFrame, dataset_name: str) -> List[str]:
        """Apply general validation rules across all datasets."""
        violations = []
        
        # Check for required automotive columns
        required_columns = {
            'basic': ['Automaker', 'Genmodel', 'Genmodel_ID'],
            'price': ['Genmodel_ID', 'Entry_price'],
            'sales': ['Genmodel_ID', 'Genmodel'],
            'trim': ['Genmodel_ID', 'Price']
        }
        
        if dataset_name in required_columns:
            missing_required = [col for col in required_columns[dataset_name] if col not in data.columns]
            if missing_required:
                violations.append(f"Missing required columns: {missing_required}")
        
        # Check for data consistency across related columns
        if 'Automaker' in data.columns and 'Genmodel' in data.columns:
            # Check for empty or whitespace-only values
            empty_automakers = (data['Automaker'].str.strip() == '').sum()
            empty_models = (data['Genmodel'].str.strip() == '').sum()
            
            if empty_automakers > 0:
                violations.append(f"Column 'Automaker' has {empty_automakers} empty values")
            
            if empty_models > 0:
                violations.append(f"Column 'Genmodel' has {empty_models} empty values")
        
        return violations

    def _calculate_overall_quality_score(self, quality_report: Dict[str, Any]) -> float:
        """Calculate overall quality score based on all assessments."""
        weights = {
            'completeness': 0.25,
            'consistency': 0.20,
            'validity': 0.20,
            'uniqueness': 0.20,
            'accuracy': 0.15
        }
        
        total_score = 0
        for category, weight in weights.items():
            if category in quality_report:
                total_score += quality_report[category]['score'] * weight
        
        return round(total_score, 1)

    def _get_quality_rating(self, quality_score: float) -> str:
        """Get quality rating based on score."""
        if quality_score >= 90:
            return 'Excellent'
        elif quality_score >= 80:
            return 'Good'
        elif quality_score >= 70:
            return 'Fair'
        elif quality_score >= 60:
            return 'Poor'
        else:
            return 'Critical'

    def _get_completeness_status(self, missing_ratio: float) -> str:
        """Get completeness status."""
        if missing_ratio <= self.quality_thresholds['missing_data_warning']:
            return 'Good'
        elif missing_ratio <= self.quality_thresholds['missing_data_error']:
            return 'Warning'
        else:
            return 'Critical'

    def _get_consistency_status(self, consistency_score: float) -> str:
        """Get consistency status."""
        if consistency_score >= 90:
            return 'Good'
        elif consistency_score >= 70:
            return 'Warning'
        else:
            return 'Critical'

    def _get_validity_status(self, validity_score: float) -> str:
        """Get validity status."""
        if validity_score >= 90:
            return 'Good'
        elif validity_score >= 70:
            return 'Warning'
        else:
            return 'Critical'

    def _get_uniqueness_status(self, duplicate_ratio: float) -> str:
        """Get uniqueness status."""
        if duplicate_ratio <= self.quality_thresholds['duplicate_threshold']:
            return 'Good'
        elif duplicate_ratio <= 0.1:
            return 'Warning'
        else:
            return 'Critical'

    def _get_accuracy_status(self, accuracy_score: float) -> str:
        """Get accuracy status."""
        if accuracy_score >= 90:
            return 'Good'
        elif accuracy_score >= 70:
            return 'Warning'
        else:
            return 'Critical'

    def _generate_quality_recommendations(self, quality_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on quality assessment."""
        recommendations = []
        
        # Completeness recommendations
        if quality_report['completeness']['score'] < 80:
            recommendations.append("Address missing data issues - consider data imputation or source verification")
        
        # Consistency recommendations
        if quality_report['consistency']['score'] < 80:
            recommendations.append("Standardize data formats and resolve consistency issues")
        
        # Validity recommendations
        if quality_report['validity']['score'] < 80:
            recommendations.append("Review and fix data validation violations")
        
        # Uniqueness recommendations
        if quality_report['uniqueness']['score'] < 80:
            recommendations.append("Remove or merge duplicate records")
        
        # Accuracy recommendations
        if quality_report['accuracy']['score'] < 80:
            recommendations.append("Investigate and resolve outlier issues")
        
        # General recommendations
        if quality_report['quality_score'] < 70:
            recommendations.append("Overall data quality needs improvement - consider comprehensive data cleaning")
        
        return recommendations

    def generate_quality_summary(self, datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Generate a comprehensive quality summary for multiple datasets."""
        summary = {
            'overall_quality': {},
            'dataset_reports': {},
            'critical_issues': [],
            'recommendations': []
        }
        
        quality_scores = []
        
        # Assess each dataset
        for name, data in datasets.items():
            if isinstance(data, pd.DataFrame):
                report = self.assess_dataset_quality(data, name)
                summary['dataset_reports'][name] = report
                quality_scores.append(report['quality_score'])
                
                # Collect critical issues
                if report['quality_rating'] == 'Critical':
                    summary['critical_issues'].append(f"{name}: {report['quality_rating']} quality")
        
        # Calculate overall metrics
        if quality_scores:
            summary['overall_quality'] = {
                'average_score': round(np.mean(quality_scores), 1),
                'min_score': min(quality_scores),
                'max_score': max(quality_scores),
                'total_datasets': len(quality_scores),
                'excellent_datasets': sum(1 for score in quality_scores if score >= 90),
                'poor_datasets': sum(1 for score in quality_scores if score < 70)
            }
        
        # Generate overall recommendations
        if summary['overall_quality'].get('average_score', 0) < 80:
            summary['recommendations'].append("Overall data quality needs attention across multiple datasets")
        
        if summary['critical_issues']:
            summary['recommendations'].append("Address critical data quality issues immediately")
        
        return summary

    def export_quality_report(self, dataset_name: str, format_type: str = 'dict') -> Any:
        """Export quality report in specified format."""
        if dataset_name not in self.quality_reports:
            return None
        
        report = self.quality_reports[dataset_name]
        
        if format_type == 'dict':
            return report.copy()
        elif format_type == 'dataframe':
            # Convert to DataFrame format
            report_data = []
            for category, details in report.items():
                if isinstance(details, dict) and 'score' in details:
                    report_data.append({
                        'category': category,
                        'score': details['score'],
                        'status': details.get('status', 'Unknown')
                    })
            return pd.DataFrame(report_data)
        elif format_type == 'json':
            import json
            return json.dumps(report, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")


# Global instance for use throughout the application
data_quality = DataQuality()

