CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    messages JSONB NOT NULL DEFAULT '[]'::jsonb,
    last_intent VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    price_per_night_bdt NUMERIC(10, 2) NOT NULL,
    max_guests INTEGER NOT NULL,
    amenities TEXT[] NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    listing_id INTEGER NOT NULL REFERENCES listings(id),
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    guests INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'confirmed',
    total_price_bdt NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
