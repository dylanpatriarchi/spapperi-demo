#!/bin/bash

# Database backup script for Spapperi RAG Agent
# Usage: ./scripts/backup-db.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/spapperi_db_${TIMESTAMP}.sql"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📦 Creating database backup...${NC}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup
docker-compose exec -T postgres pg_dump -U spapperi spapperi_rag > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✓ Backup created successfully!${NC}"
    echo "  File: $BACKUP_FILE"
    echo "  Size: $SIZE"
    
    # Keep only last 7 backups
    ls -t ${BACKUP_DIR}/spapperi_db_*.sql | tail -n +8 | xargs -r rm
    echo "  Old backups cleaned (keeping last 7)"
else
    echo "✗ Backup failed!"
    exit 1
fi


