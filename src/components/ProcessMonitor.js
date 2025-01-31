import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Table, Button, Card, Badge, Spin, Alert, Input, Space, Tooltip } from 'antd';
import { ReloadOutlined, SearchOutlined, StopOutlined, PlayCircleOutlined, WarningOutlined } from '@ant-design/icons';
import { processes } from '../services/api';
import logService from '../services/logService';
import { formatBytes, formatUptime } from '../utils/formatters';

const ProcessMonitor = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [processes, setProcesses] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);

    // Fetch processes data
    const fetchProcesses = useCallback(async () => {
        try {
            const response = await processes.list({
                search: searchText,
                sort: 'cpu_usage',
                order: 'desc'
            });
            setProcesses(response.data);
            setError(null);
            logService.debug('Processes data fetched successfully', 'PROCESS_MONITOR');
        } catch (err) {
            setError('Failed to fetch process data');
            logService.error('Failed to fetch processes', 'PROCESS_MONITOR', { error: err.message });
        } finally {
            setLoading(false);
        }
    }, [searchText]);

    // Setup periodic refresh
    useEffect(() => {
        fetchProcesses();
        const interval = setInterval(fetchProcesses, refreshInterval);
        return () => clearInterval(interval);
    }, [fetchProcesses, refreshInterval]);

    // Handle process actions
    const handleProcessAction = async (processId, action) => {
        try {
            setLoading(true);
            if (action === 'stop') {
                await processes.stop(processId);
                logService.activity('Process stopped', 'PROCESS_MONITOR', { processId });
            } else if (action === 'restart') {
                await processes.restart(processId);
                logService.activity('Process restarted', 'PROCESS_MONITOR', { processId });
            }
            await fetchProcesses();
        } catch (err) {
            setError(`Failed to ${action} process`);
            logService.error(`Process ${action} failed`, 'PROCESS_MONITOR', { 
                processId, 
                action,
                error: err.message 
            });
        }
    };

    // Table columns configuration
    const columns = useMemo(() => [
        {
            title: 'Process Name',
            dataIndex: 'name',
            sorter: true,
            render: (text, record) => (
                <Space>
                    {text}
                    {record.status === 'warning' && (
                        <Tooltip title="High resource usage">
                            <WarningOutlined style={{ color: '#faad14' }} />
                        </Tooltip>
                    )}
                </Space>
            ),
        },
        {
            title: 'Status',
            dataIndex: 'status',
            render: status => (
                <Badge 
                    status={status === 'running' ? 'success' : 'error'} 
                    text={status.charAt(0).toUpperCase() + status.slice(1)} 
                />
            ),
            filters: [
                { text: 'Running', value: 'running' },
                { text: 'Stopped', value: 'stopped' },
                { text: 'Warning', value: 'warning' },
            ],
            onFilter: (value, record) => record.status === value,
        },
        {
            title: 'CPU Usage',
            dataIndex: 'cpu_usage',
            sorter: true,
            render: value => `${value.toFixed(1)}%`,
        },
        {
            title: 'Memory Usage',
            dataIndex: 'memory_usage',
            sorter: true,
            render: value => formatBytes(value),
        },
        {
            title: 'Uptime',
            dataIndex: 'uptime',
            sorter: true,
            render: value => formatUptime(value),
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Space>
                    {record.status === 'running' ? (
                        <Button
                            icon={<StopOutlined />}
                            onClick={() => handleProcessAction(record.id, 'stop')}
                            danger
                        >
                            Stop
                        </Button>
                    ) : (
                        <Button
                            icon={<PlayCircleOutlined />}
                            onClick={() => handleProcessAction(record.id, 'restart')}
                            type="primary"
                        >
                            Start
                        </Button>
                    )}
                </Space>
            ),
        },
    ], []);

    // Search handler
    const handleSearch = value => {
        setSearchText(value);
    };

    // Refresh handler
    const handleRefresh = () => {
        setLoading(true);
        fetchProcesses();
    };

    // Row selection configuration
    const rowSelection = {
        selectedRowKeys,
        onChange: keys => setSelectedRowKeys(keys),
    };

    // Batch actions for selected processes
    const handleBatchAction = async action => {
        try {
            setLoading(true);
            await Promise.all(
                selectedRowKeys.map(processId => processes[action](processId))
            );
            logService.activity(`Batch ${action} completed`, 'PROCESS_MONITOR', { 
                processIds: selectedRowKeys 
            });
            setSelectedRowKeys([]);
            await fetchProcesses();
        } catch (err) {
            setError(`Failed to ${action} selected processes`);
            logService.error(`Batch ${action} failed`, 'PROCESS_MONITOR', { 
                processIds: selectedRowKeys,
                error: err.message 
            });
        }
    };

    return (
        <Card title="Process Monitor" className="process-monitor">
            <Space direction="vertical" style={{ width: '100%' }}>
                {error && (
                    <Alert
                        message="Error"
                        description={error}
                        type="error"
                        closable
                        onClose={() => setError(null)}
                    />
                )}

                <Space className="table-actions">
                    <Input
                        placeholder="Search processes..."
                        prefix={<SearchOutlined />}
                        onChange={e => handleSearch(e.target.value)}
                        style={{ width: 200 }}
                    />
                    <Button
                        icon={<ReloadOutlined />}
                        onClick={handleRefresh}
                        loading={loading}
                    >
                        Refresh
                    </Button>
                    {selectedRowKeys.length > 0 && (
                        <>
                            <Button
                                danger
                                onClick={() => handleBatchAction('stop')}
                            >
                                Stop Selected
                            </Button>
                            <Button
                                type="primary"
                                onClick={() => handleBatchAction('restart')}
                            >
                                Restart Selected
                            </Button>
                        </>
                    )}
                </Space>

                <Table
                    rowSelection={rowSelection}
                    columns={columns}
                    dataSource={processes}
                    loading={loading}
                    rowKey="id"
                    pagination={{
                        total: processes.length,
                        pageSize: 10,
                        showSizeChanger: true,
                        showQuickJumper: true,
                    }}
                    onChange={(pagination, filters, sorter) => {
                        // Handle table changes (sorting, filtering)
                        console.log('Table changed:', { pagination, filters, sorter });
                    }}
                />
            </Space>

            <style jsx>{`
                .process-monitor {
                    margin: 24px;
                }
                .table-actions {
                    margin-bottom: 16px;
                }
                .ant-table {
                    background: white;
                    border-radius: 8px;
                }
                .ant-table-thead > tr > th {
                    background: #fafafa;
                }
            `}</style>
        </Card>
    );
};

export default ProcessMonitor;
