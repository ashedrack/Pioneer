import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { DatePicker } from 'antd';
import dayjs from 'dayjs';
import { Card, Row, Col, Statistic } from 'antd';
const { RangePicker } = DatePicker;

interface CostData {
  month: string;
  actual: number | null;
  predicted: number | null;
}

interface CostSummary {
  total_actual: number;
  average_monthly: number;
  predicted_next_month: number;
}

interface CostResponse {
  data: CostData[];
  summary: CostSummary;
}

const CostAnalysis: React.FC = () => {
  const [costData, setCostData] = useState<CostData[]>([]);
  const [summary, setSummary] = useState<CostSummary | null>(null);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().subtract(6, 'month'),
    dayjs().add(3, 'month')
  ]);

  const fetchCostData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/metrics/cost/analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start_date: dateRange[0].format('YYYY-MM-DD'),
          end_date: dateRange[1].format('YYYY-MM-DD')
        })
      });
      
      const data: CostResponse = await response.json();
      setCostData(data.data);
      setSummary(data.summary);
    } catch (error) {
      console.error('Error fetching cost data:', error);
    }
  };

  useEffect(() => {
    fetchCostData();
  }, [dateRange]);

  const handleDateRangeChange = (dates: any) => {
    if (dates) {
      setDateRange([dates[0], dates[1]]);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  return (
    <Card title="Cost Analysis" className="dashboard-card">
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <RangePicker
            value={dateRange}
            onChange={handleDateRangeChange}
            style={{ marginBottom: 16 }}
          />
        </Col>
      </Row>
      
      {summary && (
        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={8}>
            <Statistic
              title="Total Actual Cost"
              value={summary.total_actual}
              precision={2}
              prefix="$"
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="Average Monthly Cost"
              value={summary.average_monthly}
              precision={2}
              prefix="$"
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="Predicted Next Month"
              value={summary.predicted_next_month}
              precision={2}
              prefix="$"
            />
          </Col>
        </Row>
      )}

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={costData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip
            formatter={(value: any) => formatCurrency(value)}
            labelFormatter={(label) => `Month: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="actual"
            stroke="#2196f3"
            name="Actual Cost"
            strokeWidth={2}
            dot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#ff9800"
            name="Predicted Cost"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default CostAnalysis;
