import React, { useEffect, useState } from 'react'
import http from '../http'
import { Link } from 'react-router-dom'
import { Grid, Paper, TextField, MenuItem, Button, Stack, Typography, Avatar } from '@mui/material'
import RarityChip from '../components/RarityChip'

export default function Items() {
  const [items, setItems] = useState([])
  const [q, setQ] = useState('')
  const [rarity, setRarity] = useState('')
  const [type, setType] = useState('')
  const [slot, setSlot] = useState('')
  useEffect(() => { fetchItems() }, [])

  const fetchItems = async () => {
    const params = {}
    if (q) params.name = q
    if (rarity) params.rarity = rarity
    if (type) params.type = type
    if (slot) params.slot_type = slot
    const { data } = await http.get('/api/items/', { params })
    setItems(data.body || [])
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Items</Typography>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
        <TextField size="small" label="Name" value={q} onChange={e => setQ(e.target.value)} />
        <TextField size="small" label="Rarity" value={rarity} onChange={e => setRarity(e.target.value)} select sx={{ minWidth: 160 }}>
          {['', 'Poor', 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Unique', 'Artifact'].map(r => (
            <MenuItem key={r || 'any'} value={r}>{r || 'Any'}</MenuItem>
          ))}
        </TextField>
        <TextField size="small" label="Type" value={type} onChange={e => setType(e.target.value)} select sx={{ minWidth: 160 }}>
          {['', 'Accessory', 'Armor', 'Misc', 'Utility', 'Weapon'].map(r => (
            <MenuItem key={r || 'any'} value={r}>{r || 'Any'}</MenuItem>
          ))}
        </TextField>
        <TextField size="small" label="Slot" value={slot} onChange={e => setSlot(e.target.value)} select sx={{ minWidth: 160 }}>
          {['', 'Back', 'Chest', 'Foot', 'Hands', 'Head', 'Legs', 'Necklace', 'Primary', 'Ring', 'Sash', 'Secondary', 'Unarmed', 'Utility'].map(r => (
            <MenuItem key={r || 'any'} value={r}>{r || 'Any'}</MenuItem>
          ))}
        </TextField>
        <Button onClick={fetchItems}>Search</Button>
      </Stack>
      <Grid container spacing={2}>
        {items.map(i => (
          <Grid item xs={12} sm={6} md={4} key={i.id}>
            <Paper sx={{ p: 2, display: 'flex', gap: 1, alignItems: 'center' }}>
              <Avatar variant="rounded" src={`/api/items/${i.id}/icon/`} sx={{ width: 48, height: 48 }} />
              <div>
                <Link to={`/items/${i.id}`}>{i.name}</Link>
                <div><RarityChip rarity={i.rarity} /></div>
              </div>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Stack>
  )
}


