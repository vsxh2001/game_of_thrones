-- Create enum types for status fields
CREATE TYPE season_status AS ENUM ('upcoming', 'active', 'completed');
CREATE TYPE match_status AS ENUM ('scheduled', 'in_progress', 'completed');
CREATE TYPE round_status AS ENUM ('pending', 'active', 'completed');

-- Seasons table
CREATE TABLE seasons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    status season_status DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_dates CHECK (end_date > start_date)
);

-- Teams table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    season_id INTEGER NOT NULL REFERENCES seasons(id),
    total_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_score CHECK (total_score >= 0)
);

-- Matches table
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    season_id INTEGER NOT NULL REFERENCES seasons(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status match_status DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_match_times CHECK (end_time IS NULL OR end_time > start_time)
);

-- Match Teams junction table
CREATE TABLE match_teams (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_score CHECK (score >= 0),
    CONSTRAINT unique_match_team UNIQUE (match_id, team_id)
);

CREATE INDEX idx_match_teams_match ON match_teams(match_id);
CREATE INDEX idx_match_teams_team ON match_teams(team_id);

-- Rounds table
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    round_number INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT NULL,
    duration INTEGER NOT NULL,
    gong_timedelta INTEGER NOT NULL,
    status round_status DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- Cubes table
CREATE TABLE cubes (
    id SERIAL PRIMARY KEY,
    round_id INTEGER NOT NULL REFERENCES rounds(id),
    points INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_points CHECK (points BETWEEN 1 AND 6)
);

-- Cube Control table
CREATE TABLE cube_control (
    id SERIAL PRIMARY KEY,
    cube_id INTEGER NOT NULL REFERENCES cubes(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    capture_time TIMESTAMP NOT NULL,
    release_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_control_times CHECK (release_time IS NULL OR release_time > capture_time)
);

-- Cube Takeovers table
CREATE TABLE cube_takeovers (
    id SERIAL PRIMARY KEY,
    round_id INTEGER NOT NULL REFERENCES rounds(id),
    cube_id INTEGER NOT NULL REFERENCES cubes(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    takeover_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cube_takeovers_round ON cube_takeovers(round_id);
CREATE INDEX idx_cube_takeovers_cube ON cube_takeovers(cube_id);
CREATE INDEX idx_cube_takeovers_team ON cube_takeovers(team_id);
CREATE INDEX idx_cube_takeovers_time ON cube_takeovers(takeover_time);

-- Cube Keepalives table
CREATE TABLE cube_keepalives (
    id SERIAL PRIMARY KEY,
    round_id INTEGER NOT NULL REFERENCES rounds(id),
    cube_id INTEGER NOT NULL REFERENCES cubes(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    keepalive_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cube_keepalives_round ON cube_keepalives(round_id);
CREATE INDEX idx_cube_keepalives_cube ON cube_keepalives(cube_id);
CREATE INDEX idx_cube_keepalives_team ON cube_keepalives(team_id);
CREATE INDEX idx_cube_keepalives_time ON cube_keepalives(keepalive_time);

-- Round Scores table (updated at each gong)
CREATE TABLE round_scores (
    id SERIAL PRIMARY KEY,
    round_id INTEGER NOT NULL REFERENCES rounds(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    score INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_round_team_time UNIQUE (round_id, team_id, updated_at)
);

-- Match Scores table (aggregated from rounds)
CREATE TABLE match_scores (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    score INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_match_team UNIQUE (match_id, team_id)
);

-- Season Scores table (aggregated from matches)
CREATE TABLE season_scores (
    id SERIAL PRIMARY KEY,
    season_id INTEGER NOT NULL REFERENCES seasons(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    score INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_season_team UNIQUE (season_id, team_id)
);

-- Create indexes for better performance
CREATE INDEX idx_round_scores_round ON round_scores(round_id);
CREATE INDEX idx_round_scores_team ON round_scores(team_id);
CREATE INDEX idx_round_scores_time ON round_scores(updated_at);

CREATE INDEX idx_match_scores_match ON match_scores(match_id);
CREATE INDEX idx_match_scores_team ON match_scores(team_id);
CREATE INDEX idx_match_scores_update ON match_scores(updated_at);

CREATE INDEX idx_season_scores_season ON season_scores(season_id);
CREATE INDEX idx_season_scores_team ON season_scores(team_id);
CREATE INDEX idx_season_scores_update ON season_scores(updated_at);

-- Indexes for better query performance
CREATE INDEX idx_teams_season ON teams(season_id);
CREATE INDEX idx_matches_season ON matches(season_id);
CREATE INDEX idx_rounds_match ON rounds(match_id);
CREATE INDEX idx_cubes_round ON cubes(round_id);
CREATE INDEX idx_cube_control_cube ON cube_control(cube_id);
CREATE INDEX idx_cube_control_team ON cube_control(team_id);

-- Composite indexes for common queries
CREATE INDEX idx_matches_teams ON matches(season_id, team1_id, team2_id);
CREATE INDEX idx_cube_control_timing ON cube_control(cube_id, team_id, capture_time);
