import React from 'react';
import { render, screen } from '@testing-library/react';
import RarityChip from './RarityChip';

describe('RarityChip', () => {
  it('renders with correct rarity text', () => {
    render(<RarityChip rarity="Epic" />);
    expect(screen.getByText('Epic')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Legendary', () => {
    render(<RarityChip rarity="Legendary" />);
    expect(screen.getByText('Legendary')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Common', () => {
    render(<RarityChip rarity="Common" />);
    expect(screen.getByText('Common')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Rare', () => {
    render(<RarityChip rarity="Rare" />);
    expect(screen.getByText('Rare')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Unique', () => {
    render(<RarityChip rarity="Unique" />);
    expect(screen.getByText('Unique')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Artifact', () => {
    render(<RarityChip rarity="Artifact" />);
    expect(screen.getByText('Artifact')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Poor', () => {
    render(<RarityChip rarity="Poor" />);
    expect(screen.getByText('Poor')).toBeInTheDocument();
  });

  it('renders with correct rarity text for Uncommon', () => {
    render(<RarityChip rarity="Uncommon" />);
    expect(screen.getByText('Uncommon')).toBeInTheDocument();
  });

  it('handles unknown rarity gracefully', () => {
    render(<RarityChip rarity="UnknownRarity" />);
    expect(screen.getByText('UnknownRarity')).toBeInTheDocument();
  });
});