-- Run this in the Supabase SQL Editor

-- Create kb_entries table
CREATE TABLE IF NOT EXISTS kb_entries (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT NOT NULL,
    trust_level INTEGER NOT NULL,
    category TEXT NOT NULL,
    keywords TEXT[] NOT NULL DEFAULT '{}',
    intents TEXT[] NOT NULL DEFAULT '{}',
    controversial BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create contradiction_groups table
CREATE TABLE IF NOT EXISTS contradiction_groups (
    group_name TEXT PRIMARY KEY,
    entry_ids TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Set Row Level Security (RLS) to allow all operations for now (or adjust as needed)
ALTER TABLE kb_entries DISABLE ROW LEVEL SECURITY;
ALTER TABLE contradiction_groups DISABLE ROW LEVEL SECURITY;
