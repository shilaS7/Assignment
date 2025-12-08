#!/bin/bash

# Script to extract test report with timestamp

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="reports"
REPORT_NAME="test_report_${TIMESTAMP}.html"

# Create reports directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Copy the current report to reports directory with timestamp
if [ -f "report.html" ]; then
    cp report.html "${REPORT_DIR}/${REPORT_NAME}"
    echo "✅ Report extracted to: ${REPORT_DIR}/${REPORT_NAME}"
    echo "📊 Report size: $(ls -lh "${REPORT_DIR}/${REPORT_NAME}" | awk '{print $5}')"
    
    # Optionally open the report
    if [ "$1" == "--open" ]; then
        open "${REPORT_DIR}/${REPORT_NAME}"
    fi
else
    echo "❌ report.html not found. Run tests first to generate a report."
    exit 1
fi

