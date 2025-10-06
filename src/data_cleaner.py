"""
🧹 Data Cleaning Module for Car Market Analysis

Robust and reusable data cleaning functions for automotive market data.
Handles data quality issues, standardization, and validation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


def clean_automaker_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y estandariza la columna 'Automaker' del dataframe.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Automaker' a limpiar

    Returns:
        pd.DataFrame: DataFrame con datos limpios

    Funcionalidades:
    - Corrige nombres de fabricantes conocidos incorrectos
    - Elimina filas con fabricantes no deseados como 'undefined'
    - Estandariza formato y elimina espacios extra
    - Valida consistencia de datos
    """
    if df.empty or 'Automaker' not in df.columns:
        print("⚠️  DataFrame vacío o sin columna 'Automaker'")
        return df

    # Guardar estado inicial para reporte
    initial_count = len(df)
    initial_automakers = df['Automaker'].nunique()

    print(f"Iniciando limpieza de datos Automaker...")
    print(f"   - Filas iniciales: {initial_count:,}")
    print(f"   - Fabricantes unicos iniciales: {initial_automakers}")

    # Diccionario de mapeo para corregir fabricantes incorrectos
    # Basado en hallazgos del análisis exploratorio
    automaker_mapping = {
        # Modelos mal clasificados como fabricantes
        'Sebring': 'Chrysler',
        'PT Cruiser': 'Chrysler',
        'Town & Country': 'Chrysler',
        '300C': 'Chrysler',
        'Crossfire': 'Chrysler',
        
        # Nombres alternativos o variaciones
        'Mercedes': 'Mercedes-Benz',
        'BMW Group': 'BMW',
        'VW': 'Volkswagen',
        'VW Group': 'Volkswagen',
        
        # Posibles errores de tipeo comunes
        'Audi AG': 'Audi',
        'Toyota Motor': 'Toyota',
        'Ford Motor': 'Ford',
        'General Motors': 'GM',
        'Chrysler Group': 'Chrysler',
        
        # Fabricantes con nombres inconsistentes
        'Range Rover': 'Land Rover',
        'Jaguar Land Rover': 'Jaguar',  # O 'Land Rover' dependiendo del contexto
        
        # Agregar más correcciones según hallazgos específicos
    }

    # Aplicar las correcciones de mapeo
    corrections_made = 0
    for old_name, new_name in automaker_mapping.items():
        mask = df['Automaker'] == old_name
        if mask.any():
            count = mask.sum()
            df.loc[mask, 'Automaker'] = new_name
            corrections_made += count
            print(f"   + Corregido '{old_name}' -> '{new_name}' ({count} registros)")

    # Eliminar filas con fabricantes problemáticos o no deseados
    problematic_values = [
        'undefined', 'Undefined', 'UNDEFINED',
        'unknown', 'Unknown', 'UNKNOWN',
        'null', 'NULL', 'None', 'N/A', 'n/a',
        '', ' ', '  ', '   ',  # Espacios en blanco
        'TBD', 'tbd', 'To Be Determined',
        'Other', 'Misc', 'Miscellaneous'
    ]

    # Crear máscara para valores problemáticos
    problematic_mask = df['Automaker'].str.lower().isin([v.lower() for v in problematic_values])
    problematic_mask |= df['Automaker'].str.strip().isin(['', ' ', '  '])
    
    removed_count = problematic_mask.sum()
    if removed_count > 0:
        df = df[~problematic_mask].copy()
        print(f"   + Eliminadas {removed_count} filas con valores problematicos")

    # Estandarizar formato: eliminar espacios extra y normalizar
    df['Automaker'] = df['Automaker'].str.strip()
    df['Automaker'] = df['Automaker'].str.replace(r'\s+', ' ', regex=True)  # Múltiples espacios → un espacio

    # Validar que no queden valores vacíos después de la limpieza
    empty_mask = (df['Automaker'].str.strip() == '') | df['Automaker'].isna()
    if empty_mask.any():
        df = df[~empty_mask].copy()
        print(f"   + Eliminadas {empty_mask.sum()} filas con valores vacios finales")

    # Reporte final
    final_count = len(df)
    final_automakers = df['Automaker'].nunique()
    removed_total = initial_count - final_count

    print(f"\nRESUMEN DE LIMPIEZA:")
    print(f"   - Filas finales: {final_count:,}")
    print(f"   - Fabricantes unicos finales: {final_automakers}")
    print(f"   - Filas eliminadas: {removed_total:,} ({removed_total/initial_count*100:.1f}%)")
    print(f"   - Correcciones aplicadas: {corrections_made}")
    
    if final_count > 0:
        print(f"   OK - Limpieza completada exitosamente")
    else:
        print(f"   ADVERTENCIA - No quedaron datos despues de la limpieza")

    return df


def validate_automaker_consistency(df: pd.DataFrame) -> Dict[str, any]:
    """
    Valida la consistencia de los datos de fabricantes después de la limpieza.

    Args:
        df (pd.DataFrame): DataFrame limpio para validar

    Returns:
        Dict: Reporte de validación con métricas y alertas
    """
    if df.empty or 'Automaker' not in df.columns:
        return {'status': 'error', 'message': 'DataFrame vacío o sin columna Automaker'}

    validation_report = {
        'status': 'success',
        'total_records': len(df),
        'unique_automakers': df['Automaker'].nunique(),
        'issues': [],
        'recommendations': []
    }

    # Verificar valores nulos
    null_count = df['Automaker'].isnull().sum()
    if null_count > 0:
        validation_report['issues'].append(f"{null_count} valores nulos encontrados")

    # Verificar valores vacíos
    empty_count = (df['Automaker'].str.strip() == '').sum()
    if empty_count > 0:
        validation_report['issues'].append(f"{empty_count} valores vacíos encontrados")

    # Verificar duplicados (esto puede ser normal para fabricantes)
    duplicate_count = df.duplicated(subset=['Automaker']).sum()
    if duplicate_count > 0:
        validation_report['issues'].append(f"{duplicate_count} filas duplicadas encontradas")

    # Verificar fabricantes con muy pocos modelos (posible error)
    automaker_counts = df['Automaker'].value_counts()
    low_count_automakers = automaker_counts[automaker_counts == 1]
    if len(low_count_automakers) > 0:
        validation_report['recommendations'].append(
            f"{len(low_count_automakers)} fabricantes con solo 1 modelo - verificar si son errores"
        )

    # Verificar fabricantes con nombres sospechosos
    suspicious_patterns = ['test', 'demo', 'sample', 'xxx', 'zzz']
    for pattern in suspicious_patterns:
        suspicious = df[df['Automaker'].str.lower().str.contains(pattern, na=False)]
        if not suspicious.empty:
            validation_report['issues'].append(f"Fabricantes sospechosos con patrón '{pattern}': {suspicious['Automaker'].unique()}")

    # Calcular score de calidad
    quality_score = 100
    quality_score -= len(validation_report['issues']) * 10
    quality_score -= len(validation_report['recommendations']) * 5
    quality_score = max(0, quality_score)
    
    validation_report['quality_score'] = quality_score
    validation_report['quality_status'] = (
        'excellent' if quality_score >= 90 else
        'good' if quality_score >= 70 else
        'fair' if quality_score >= 50 else
        'poor'
    )

    return validation_report


def clean_genmodel_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y estandariza la columna 'Genmodel' del dataframe.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Genmodel' a limpiar

    Returns:
        pd.DataFrame: DataFrame con datos limpios
    """
    if df.empty or 'Genmodel' not in df.columns:
        print("⚠️  DataFrame vacío o sin columna 'Genmodel'")
        return df

    print(f"🔍 Limpiando datos Genmodel...")

    # Eliminar espacios extra
    df['Genmodel'] = df['Genmodel'].str.strip()
    df['Genmodel'] = df['Genmodel'].str.replace(r'\s+', ' ', regex=True)

    # Eliminar valores problemáticos
    problematic_models = ['undefined', 'unknown', 'null', '', 'TBD']
    mask = df['Genmodel'].str.lower().isin([v.lower() for v in problematic_models])
    if mask.any():
        df = df[~mask].copy()
        print(f"   ✓ Eliminados {mask.sum()} modelos problemáticos")

    return df


def clean_all_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, any]]:
    """
    Limpieza completa de todos los datos del dataframe.

    Args:
        df (pd.DataFrame): DataFrame a limpiar

    Returns:
        Tuple[pd.DataFrame, Dict]: DataFrame limpio y reporte de limpieza
    """
    cleaning_report = {
        'initial_shape': df.shape,
        'steps_completed': [],
        'final_shape': None,
        'validation_report': None
    }

    # Paso 1: Limpiar Automaker
    if 'Automaker' in df.columns:
        df = clean_automaker_data(df)
        cleaning_report['steps_completed'].append('automaker_cleaning')

    # Paso 2: Limpiar Genmodel
    if 'Genmodel' in df.columns:
        df = clean_genmodel_data(df)
        cleaning_report['steps_completed'].append('genmodel_cleaning')

    # Paso 3: Validar resultados
    if 'Automaker' in df.columns:
        validation_report = validate_automaker_consistency(df)
        cleaning_report['validation_report'] = validation_report

    cleaning_report['final_shape'] = df.shape

    return df, cleaning_report


# Función de utilidad para mostrar reporte de limpieza
def print_cleaning_report(report: Dict[str, any]) -> None:
    """Imprime un reporte detallado de la limpieza de datos."""
    print("\n" + "="*60)
    print("📋 REPORTE DE LIMPIEZA DE DATOS")
    print("="*60)
    
    print(f"📊 Dimensiones:")
    print(f"   • Inicial: {report['initial_shape']}")
    print(f"   • Final: {report['final_shape']}")
    
    print(f"\n🔧 Pasos completados:")
    for step in report['steps_completed']:
        print(f"   ✓ {step.replace('_', ' ').title()}")
    
    if report['validation_report']:
        validation = report['validation_report']
        print(f"\n🎯 Validación:")
        print(f"   • Score de calidad: {validation['quality_score']}/100 ({validation['quality_status']})")
        print(f"   • Registros totales: {validation['total_records']:,}")
        print(f"   • Fabricantes únicos: {validation['unique_automakers']}")
        
        if validation['issues']:
            print(f"\n⚠️  Problemas encontrados:")
            for issue in validation['issues']:
                print(f"   • {issue}")
        
        if validation['recommendations']:
            print(f"\n💡 Recomendaciones:")
            for rec in validation['recommendations']:
                print(f"   • {rec}")
    
    print("="*60)
