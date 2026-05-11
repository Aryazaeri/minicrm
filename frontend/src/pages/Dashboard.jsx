import { useEffect, useState } from 'react'
import api from '../api'

const StatCard = ({ label, value, color }) => (
  <div className="bg-white border border-gray-200 rounded-xl p-5">
    <p className="text-sm text-gray-500 mb-1">{label}</p>
    <p className={`text-3xl font-semibold ${color}`}>{value}</p>
  </div>
)

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('/leads/dashboard/stats').then(r => setStats(r.data))
  }, [])

  if (!stats) return <p className="text-gray-400">Loading...</p>

  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">Dashboard</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total leads" value={stats.total_leads} color="text-gray-800" />
        <StatCard label="Pipeline value" value={`$${stats.total_value.toLocaleString()}`} color="text-indigo-600" />
        <StatCard label="Won" value={stats.won} color="text-green-600" />
        <StatCard label="Lost" value={stats.lost} color="text-red-500" />
      </div>
      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <p className="text-sm text-gray-500 mb-1">Leads in progress</p>
        <p className="text-3xl font-semibold text-amber-500">{stats.in_progress}</p>
      </div>
    </div>
  )
}
