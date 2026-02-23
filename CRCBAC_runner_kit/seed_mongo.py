"""Seed a minimal MongoDB dataset to run CRCBAC_code smoke tests.

This seeds the collections referenced directly in CRBAC_Gateway_Grant_transfer.py:
  - CRBAC_Policies.GRT_dev500_R100_20ctx
  - CRBAC_Policies.GRT_Role_ctx_policy500
  - (optional but recommended for running as-is) throughput_file1, p1k_rolectx_res10,
    GRT_Role_ctx_policy4000, GRT_Role_ctx_policy5000

Usage:
  python seed_mongo.py

Prereq:
  MongoDB running on mongodb://localhost:27017
"""

from __future__ import annotations

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "CRBAC_Policies"


def upsert_many(coll, docs, key_fields):
    for d in docs:
        q = {k: d[k] for k in key_fields}
        coll.update_one(q, {"$set": d}, upsert=True)


def main() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Role assignment: choose roles that satisfy the built-in hierarchy check:
    # grant requires role_t parent of role_n. In their tree, R1 is parent of R6.
    role_assign = [
        {"Id": "idT", "Context": "ctxT", "Role": "R1"},
        {"Id": "idN", "Context": "ctxN", "Role": "R6"},
    ]

    upsert_many(db["GRT_dev500_R100_20ctx"], role_assign, key_fields=["Id", "Context"])

    # Policies: role_t has capability capA in ctxT (allow). This enables the grant operation.
    pol = [
        {"Role": "R1", "Context": "ctxT", "Capability": "capA", "Permission": "allow"},
        # also add a deny example (optional)
        {"Role": "R6", "Context": "ctxN", "Capability": "capB", "Permission": "deny"},
    ]

    # The gateway checks for this collection name at startup.
    upsert_many(db["GRT_Role_ctx_policy500"], pol, key_fields=["Role", "Context", "Capability"])

    # The gateway script also references these names in different branches.
    upsert_many(db["GRT_Role_ctx_policy4000"], pol, key_fields=["Role", "Context", "Capability"])
    upsert_many(db["GRT_Role_ctx_policy5000"], pol, key_fields=["Role", "Context", "Capability"])

    # For the AC (access check) branch, it uses throughput_file1 and p1k_rolectx_res10.
    upsert_many(db["throughput_file1"], role_assign, key_fields=["Id", "Context"])
    upsert_many(db["p1k_rolectx_res10"], pol, key_fields=["Role", "Context", "Capability"])

    print("Seed complete.")
    print("DB:", DB_NAME)
    print("Collections seeded:", ", ".join(sorted(db.list_collection_names())))


if __name__ == "__main__":
    main()
