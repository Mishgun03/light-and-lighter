import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import http from '../http'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, AreaChart, Area } from 'recharts'
import { Paper, Typography, Stack, Button } from '@mui/material'
import { authHeaders } from '../auth'

export default function ItemDetail() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [market, setMarket] = useState([])
  const [history, setHistory] = useState([])
  useEffect(() => {
    http.get(`/api/items/${id}/`).then(r => setData(r.data)).catch(() => setData(null))
    http.get(`/api/items/${id}/market/`).then(r => setMarket(r.data.body || [])).catch(() => setMarket([]))
    http.get(`/api/items/${id}/history/`, { params: { interval: '1h' } }).then(r => setHistory(r.data || [])).catch(() => setHistory([]))
  }, [id])
  async function addFavorite() {
    await http.post('/api/favorites/', { item_id: id }).catch(() => {})
    alert('Added to favorites')
  }
  async function removeFavorite() {
    await http.post('/api/favorites/remove/', { item_id: id }).catch(() => {})
    alert('Removed from favorites')
  }

  if (!data) return <div>Loading...</div>
  const item = data.body || data
  return (
    <Stack spacing={2}>
      <Stack direction="row" spacing={2} alignItems="center">
        <Avatar variant="rounded" src={`/api/items/${id}/icon/`} sx={{ width: 56, height: 56 }} />
        <div>
          <Typography variant="h5">{item.name}</Typography>
          <Typography color="text.secondary">Rarity: {item.rarity}</Typography>
        </div>
      </Stack>
      <Stack direction="row" spacing={1}>
        <Button onClick={addFavorite}>Favorite</Button>
        <Button color="secondary" onClick={removeFavorite}>Unfavorite</Button>
      </Stack>
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>Price History</Typography>
        <div style={{ height: 280 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={history.map(d => ({ ...d, ts: new Date(d.created_at || d.timestamp).toLocaleString() }))}>
              <defs>
                <linearGradient id="colorAvg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.5}/>
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ts" minTickGap={32} />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey={history[0]?.price !== undefined ? 'price' : 'avg'} stroke="#8884d8" fillOpacity={1} fill="url(#colorAvg)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Paper>
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>Recent Listings</Typography>
        <ul>
          {market.map(m => (
            <li key={m.id}>{new Date(m.created_at).toLocaleString()} — {m.price}g (qty {m.quantity})</li>
          ))}
        </ul>
      </Paper>
    </Stack>
  )
}


