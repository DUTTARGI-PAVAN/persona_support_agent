# API Troubleshooting Guide

## 401 Unauthorized Error

Cause:
- Invalid API key
- Expired authentication token
- Incorrect Authorization header

Resolution:
1. Verify the API key is active.
2. Ensure the Authorization header follows:
   Authorization: Bearer YOUR_API_KEY
3. Generate a new API key if needed.

## 403 Forbidden Error

Cause:
- Insufficient permissions

Resolution:
1. Verify account permissions.
2. Contact the administrator.

## 429 Too Many Requests

Cause:
- Rate limit exceeded

Resolution:
1. Reduce request frequency.
2. Implement retry logic with exponential backoff.