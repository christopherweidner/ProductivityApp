import { useState, useEffect } from 'react'
import axios from 'axios'
import { Activity, Play, Square, AlertCircle, CheckCircle, Timer, Coffee } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const API_URL = 'http://localhost:5001/api'

function App() {
  const [isRunning, setIsRunning] = useState(false)
  const [mode, setMode] = useState('IDLE')
  const [timeLeft, setTimeLeft] = useState(0)
  const [logs, setLogs] = useState([])
  const [stats, setStats] = useState({ productive: 0, wasteful: 0 })

  useEffect(() => {
    fetchStatus()
    fetchLogs()
    const interval = setInterval(() => {
      fetchStatus()
      fetchLogs()
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_URL}/status`)
      setIsRunning(res.data.running)
      setMode(res.data.mode || 'IDLE')
      setTimeLeft(res.data.time_remaining || 0)
    } catch (err) {
      console.error("Error fetching status:", err)
    }
  }

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API_URL}/logs`)
      setLogs(res.data)
      calculateStats(res.data)
    } catch (err) {
      console.error("Error fetching logs:", err)
    }
  }

  const calculateStats = (data) => {
    let prod = 0
    let waste = 0
    data.forEach(item => {
      if (item.Classification === 'Productive') prod++
      if (item.Classification === 'Wasteful') waste++
    })
    setStats({ productive: prod, wasteful: waste })
  }

  const handleStart = async () => {
    try {
      await axios.post(`${API_URL}/start`)
      setIsRunning(true)
    } catch (err) {
      console.error("Error starting agent:", err)
    }
  }

  const handleStop = async () => {
    try {
      await axios.post(`${API_URL}/stop`)
      setIsRunning(false)
    } catch (err) {
      console.error("Error stopping agent:", err)
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const chartData = [
    { name: 'Productive', value: stats.productive },
    { name: 'Wasteful', value: stats.wasteful },
  ]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">

        {/* Header */}
        <header className="flex items-center justify-between border-b border-gray-800 pb-6">
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-blue-500" />
            <h1 className="text-3xl font-bold tracking-tight">Deep Work Agent</h1>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            <span className="text-sm font-medium text-gray-400">{isRunning ? 'ACTIVE' : 'STOPPED'}</span>
          </div>
        </header>

        {/* Timer & Controls */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-lg flex flex-col items-center justify-center gap-6 relative overflow-hidden">

            {/* Background Glow */}
            <div className={`absolute inset-0 opacity-10 ${mode === 'WORK' ? 'bg-blue-500' : mode === 'BREAK' ? 'bg-green-500' : 'bg-gray-500'
              }`} />

            <div className="text-center space-y-2 z-10">
              <div className="flex items-center justify-center gap-2 text-gray-400 mb-2">
                {mode === 'WORK' ? <Timer className="w-5 h-5" /> : mode === 'BREAK' ? <Coffee className="w-5 h-5" /> : <Square className="w-5 h-5" />}
                <span className="font-medium tracking-wider">{mode === 'IDLE' ? 'READY' : mode}</span>
              </div>
              <div className="text-6xl font-mono font-bold tracking-tighter">
                {formatTime(timeLeft)}
              </div>
            </div>

            <div className="flex gap-4 z-10">
              <button
                onClick={handleStart}
                disabled={isRunning}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold transition-all ${isRunning
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-900/20 shadow-lg'
                  }`}
              >
                <Play className="w-5 h-5" /> Start Focus
              </button>
              <button
                onClick={handleStop}
                disabled={!isRunning}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold transition-all ${!isRunning
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                    : 'bg-red-600 hover:bg-red-500 text-white shadow-red-900/20 shadow-lg'
                  }`}
              >
                <Square className="w-5 h-5" /> Stop Session
              </button>
            </div>
          </div>

          {/* Stats */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Performance</h2>
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical">
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" width={80} tick={{ fill: '#9ca3af' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#f3f4f6' }}
                    cursor={{ fill: 'transparent' }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={32}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === 'Productive' ? '#3b82f6' : '#ef4444'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Logs */}
        <div className="bg-gray-900 rounded-xl border border-gray-800 shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-800">
            <h2 className="text-xl font-semibold">Activity Log</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-gray-400">
              <thead className="bg-gray-950 text-gray-200 uppercase font-medium">
                <tr>
                  <th className="px-6 py-4">Time</th>
                  <th className="px-6 py-4">App</th>
                  <th className="px-6 py-4">Title</th>
                  <th className="px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {logs.slice().reverse().map((log, i) => (
                  <tr key={i} className="hover:bg-gray-800/50 transition-colors">
                    <td className="px-6 py-4 font-mono text-xs">{new Date(log.Timestamp).toLocaleTimeString()}</td>
                    <td className="px-6 py-4 font-medium text-gray-300">{log.App}</td>
                    <td className="px-6 py-4 truncate max-w-xs" title={log.Title}>{log.Title}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${log.Classification === 'Productive'
                          ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                          : 'bg-red-500/10 text-red-400 border border-red-500/20'
                        }`}>
                        {log.Classification === 'Productive' ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                        {log.Classification}
                      </span>
                    </td>
                  </tr>
                ))}
                {logs.length === 0 && (
                  <tr>
                    <td colSpan="4" className="px-6 py-8 text-center text-gray-500">No activity logged yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  )
}

export default App
