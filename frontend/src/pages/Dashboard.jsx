import React, { useEffect, useState } from 'react'
import http from '../http'
import { Paper, Typography, Grid, List, ListItem, ListItemText } from '@mui/material'

export default function Dashboard() {
  const [data, setData] = useState(null)
  useEffect(() => {
    http.get('/api/dashboard/').then(r => setData(r.data)).catch(() => setData({}))
  }, [])
  const population = data?.population
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>Dashboard</Typography>
      </Grid>
      {population && (
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>Online Now</Typography>
            <Typography>Online: {population.num_online}</Typography>
            <Typography>Lobby: {population.num_lobby}</Typography>
            <Typography>Dungeon: {population.num_dungeon}</Typography>
          </Paper>
        </Grid>
      )}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>Your Favorites</Typography>
          {(!data?.favorites || data.favorites.length === 0) && <Typography color="text.secondary">No favorites yet.</Typography>}
          {!!data?.favorites?.length && (
            <List dense>
              {data.favorites.map(f => (
                <ListItem key={f.id} divider>
                  <ListItemText
                    primary={`${f.item.name} (${f.item.rarity})`}
                    secondary={f.latest_price?.price ? `${f.latest_price.price}g` : '—'}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </Paper>
      </Grid>
    </Grid>
  )
}


