"""
MongoDB index migrations for the SND database.

Run with: python migrations/migrate.py  (from the project root inside the api container)
Reads connection config from environment variables (same as the API).
"""
import asyncio
import os
import sys

from motor import motor_asyncio
from pymongo import ASCENDING, TEXT


DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 27017))
DATABASE_NAME = os.getenv("DATABASE_NAME", "snd")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")


def get_client():
    if DATABASE_USERNAME:
        uri = f"mongodb://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        return motor_asyncio.AsyncIOMotorClient(uri)
    return motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)


MIGRATIONS = []


def migration(fn):
    MIGRATIONS.append(fn)
    return fn


@migration
async def m001_person_code_unique_index(db):
    """Unique index on person.code — used as URL slug and must be unique."""
    await db["person"].create_index([("code", ASCENDING)], unique=True, name="idx_person_code_unique")
    print("  [OK] person.code unique index")


@migration
async def m002_person_text_search_index(db):
    """Full-text search index on person names for the /person/all?s= endpoint."""
    await db["person"].create_index(
        [
            ("last_name", TEXT),
            ("first_name", TEXT),
            ("middle_name", TEXT),
        ],
        name="idx_person_text_search",
        default_language="russian",
    )
    print("  [OK] person text search index (last_name, first_name, middle_name)")


@migration
async def m003_person_status_index(db):
    """Index on person.status for filtering by status in listings."""
    await db["person"].create_index([("status", ASCENDING)], name="idx_person_status")
    print("  [OK] person.status index")


@migration
async def m004_person_score_index(db):
    """Descending index on person.score for sorted listings."""
    from pymongo import DESCENDING
    await db["person"].create_index([("score", DESCENDING)], name="idx_person_score_desc")
    print("  [OK] person.score descending index")


@migration
async def m005_person_deleted_at_index(db):
    """Index on person.deleted_at to efficiently filter soft-deleted records."""
    await db["person"].create_index([("deleted_at", ASCENDING)], name="idx_person_deleted_at")
    print("  [OK] person.deleted_at index")


@migration
async def m006_user_email_unique_index(db):
    """Unique index on users.email — login key."""
    await db["users"].create_index([("email", ASCENDING)], unique=True, name="idx_users_email_unique")
    print("  [OK] users.email unique index")


@migration
async def m007_military_unit_number_index(db):
    """Index on militaryunit.number for lookups by unit number."""
    await db["militaryunit"].create_index([("number", ASCENDING)], name="idx_militaryunit_number")
    print("  [OK] militaryunit.number index")


async def run_migrations():
    client = get_client()
    db = client[DATABASE_NAME]

    print(f"Connecting to MongoDB at {DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

    # Use a simple metadata collection to track applied migrations
    meta = db["_migrations"]

    applied = {doc["name"] async for doc in meta.find({}, {"name": 1})}
    print(f"Already applied: {len(applied)} migration(s)\n")

    ran = 0
    for fn in MIGRATIONS:
        name = fn.__name__
        if name in applied:
            print(f"  [SKIP] {name}")
            continue
        print(f"  [RUN ] {name}: {fn.__doc__.strip().splitlines()[0]}")
        try:
            await fn(db)
            await meta.insert_one({"name": name})
            ran += 1
        except Exception as exc:
            print(f"  [FAIL] {name}: {exc}", file=sys.stderr)
            raise

    print(f"\nDone. Ran {ran} new migration(s).")
    client.close()


if __name__ == "__main__":
    asyncio.run(run_migrations())
