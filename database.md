-- SQLite schema for initial prototype
-- Enable foreign key support
PRAGMA foreign_keys = ON;

/*--------------------------------------------------------------------
  vehicles
--------------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS Vehicle (
    id               INTEGER PRIMARY KEY,
    make             TEXT    NOT NULL,
    model            TEXT    NOT NULL,
    year             INTEGER NOT NULL,
    vin              TEXT    UNIQUE,
    purchase_price_c NUMERIC(10, 2) NOT NULL,
    auction_fee_c    NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status           TEXT    NOT NULL CHECK (status IN ('purchased', 'parted_out', 'closed_out')),
    purchased_dt     TEXT    NOT NULL DEFAULT (datetime('now'))
);

/*--------------------------------------------------------------------
  parts
--------------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS Parts (
    id               INTEGER PRIMARY KEY,
    vehicle_id       INTEGER NOT NULL,
    name             TEXT    NOT NULL,
    oem_number       TEXT,
    condition_note   TEXT,
    loc_locker       TEXT    NOT NULL,
    loc_bin          TEXT    NOT NULL,
    est_value_c      NUMERIC(10, 2) NOT NULL,
    status           TEXT    NOT NULL CHECK (status IN ('in_bin', 'listed', 'sold', 'scrapped')),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

/*--------------------------------------------------------------------
  listings
--------------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS Listings (
    id           INTEGER PRIMARY KEY,
    part_id      INTEGER NOT NULL,
    platform     TEXT    NOT NULL CHECK (platform IN ('ebay', 'facebook', 'shopify', 'local')),
    external_id  TEXT,
    url          TEXT,
    price_c      NUMERIC(10, 2) NOT NULL,
    fees_c       NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status       TEXT    NOT NULL CHECK (status IN ('draft', 'live', 'sold', 'ended')),
    listed_dt    TEXT    NOT NULL,
    sold_dt      TEXT,
    FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE
);

/*--------------------------------------------------------------------
  Indexes for performance
--------------------------------------------------------------------*/
CREATE INDEX IF NOT EXISTS idx_parts_vehicle_id   ON parts(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_listings_part_id   ON listings(part_id);
