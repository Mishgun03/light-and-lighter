import React from "react";
import { Chip } from "@mui/material";

const colors = {
  Poor: { bg: "#6b7280", fg: "#fff" },
  Uncommon: { bg: "#6b7280", fg: "#fff" },
  Common: { bg: "#e5e7eb", fg: "#111827" },
  Rare: { bg: "#3b82f6", fg: "#fff" },
  Epic: { bg: "#8b5cf6", fg: "#fff" },
  Legendary: { bg: "#f59e0b", fg: "#111827" },
  Unique: { bg: "#b45309", fg: "#fff" },
  Artifact: { bg: "#0ea5e9", fg: "#fff" },
};

export default function RarityChip({ rarity }) {
  const c = colors[rarity] || { bg: "#374151", fg: "#fff" };
  return (
    <Chip size="small" label={rarity} sx={{ bgcolor: c.bg, color: c.fg }} />
  );
}
