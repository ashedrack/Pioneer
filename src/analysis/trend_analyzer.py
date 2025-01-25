import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TrendAnalyzer:
    def __init__(self, config: Dict[str, Any]):
        self.client = InfluxDBClient(
            url=config['url'],
            token=config['token'],
            org=config['org']
        )
        self.query_api = self.client.query_api()
        self.bucket = config['bucket']

    def analyze_resource_patterns(self, resource_id: str, metric_name: str, 
                                days: int = 30) -> Dict[str, Any]:
        """Analyze resource usage patterns over the specified period."""
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -{days}d)
            |> filter(fn: (r) => r["_measurement"] == "{metric_name}")
            |> filter(fn: (r) => r["resource_id"] == "{resource_id}")
            |> aggregateWindow(every: 1h, fn: mean)
        '''
        
        result = self.query_api.query_data_frame(query)
        if result.empty:
            return {}
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(result)
        df['_time'] = pd.to_datetime(df['_time'])
        df.set_index('_time', inplace=True)
        
        # Add hour and day of week
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        
        analysis = {
            'patterns': self._identify_patterns(df),
            'idle_periods': self._find_idle_periods(df),
            'peak_periods': self._find_peak_periods(df),
            'recommendations': self._generate_recommendations(df)
        }
        
        return analysis
    
    def _identify_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify recurring patterns in the data."""
        patterns = {
            'hourly_avg': df.groupby('hour')['_value'].mean().to_dict(),
            'daily_avg': df.groupby('day_of_week')['_value'].mean().to_dict(),
            'variability': df['_value'].std()
        }
        return patterns
    
    def _find_idle_periods(self, df: pd.DataFrame, threshold: float = 20.0) -> List[Dict]:
        """Find periods of low resource utilization."""
        idle_periods = []
        
        # Group by hour and day of week
        hourly_avg = df.groupby(['day_of_week', 'hour'])['_value'].mean()
        
        for (day, hour), value in hourly_avg.items():
            if value < threshold:
                idle_periods.append({
                    'day_of_week': day,
                    'hour': hour,
                    'avg_utilization': value
                })
        
        return idle_periods
    
    def _find_peak_periods(self, df: pd.DataFrame, threshold: float = 80.0) -> List[Dict]:
        """Find periods of high resource utilization."""
        peak_periods = []
        
        # Group by hour and day of week
        hourly_avg = df.groupby(['day_of_week', 'hour'])['_value'].mean()
        
        for (day, hour), value in hourly_avg.items():
            if value > threshold:
                peak_periods.append({
                    'day_of_week': day,
                    'hour': hour,
                    'avg_utilization': value
                })
        
        return peak_periods
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate optimization recommendations based on usage patterns."""
        recommendations = []
        
        # Analyze daily patterns
        daily_avg = df.groupby('day_of_week')['_value'].mean()
        low_usage_days = daily_avg[daily_avg < 20].index
        
        if len(low_usage_days) > 0:
            days = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][d] for d in low_usage_days]
            recommendations.append(f"Consider scaling down resources on {', '.join(days)}")
        
        # Analyze hourly patterns
        hourly_avg = df.groupby('hour')['_value'].mean()
        low_usage_hours = hourly_avg[hourly_avg < 20].index
        
        if len(low_usage_hours) > 0:
            hours_str = ', '.join([f"{h:02d}:00" for h in low_usage_hours])
            recommendations.append(f"Consider scaling down resources during hours: {hours_str}")
        
        return recommendations
