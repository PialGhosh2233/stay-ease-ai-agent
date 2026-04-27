# API Contract

## POST `/api/chat/{conversation_id}/message`

Send one guest message to the StayEase AI agent and receive the assistant response for the current turn.

### Path Parameters

| Name | Type | Description |
| --- | --- | --- |
| `conversation_id` | `string (UUID)` | Unique ID for the guest conversation. |

### Request Body

```json
{
  "message": "I need a room in Cox's Bazar from 2026-05-10 to 2026-05-12 for 2 guests"
}
```

### Response Body

```json
{
  "conversation_id": "8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb",
  "intent": "search",
  "response": "I found 2 available properties in Cox's Bazar: Sea View Apartment for BDT 4,500/night and Coral Reef Studio for BDT 3,800/night.",
  "messages": [
    {
      "role": "guest",
      "content": "I need a room in Cox's Bazar from 2026-05-10 to 2026-05-12 for 2 guests"
    },
    {
      "role": "assistant",
      "content": "I found 2 available properties in Cox's Bazar: Sea View Apartment for BDT 4,500/night and Coral Reef Studio for BDT 3,800/night."
    }
  ]
}
```

### Example

Request:

```http
POST /api/chat/8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb/message
Content-Type: application/json
```

```json
{
  "message": "Show me available stays in Sylhet from 2026-06-14 to 2026-06-16 for 3 guests"
}
```

Response:

```json
{
  "conversation_id": "8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb",
  "intent": "search",
  "response": "I found 1 available property in Sylhet: Tea Garden Retreat for BDT 5,200/night.",
  "messages": [
    {
      "role": "guest",
      "content": "Show me available stays in Sylhet from 2026-06-14 to 2026-06-16 for 3 guests"
    },
    {
      "role": "assistant",
      "content": "I found 1 available property in Sylhet: Tea Garden Retreat for BDT 5,200/night."
    }
  ]
}
```

### Possible Error Responses

`400 Bad Request`

```json
{
  "detail": "message must not be empty"
}
```

`404 Not Found`

```json
{
  "detail": "conversation not found"
}
```

`422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

`500 Internal Server Error`

```json
{
  "detail": "failed to process guest message"
}
```

## GET `/api/chat/{conversation_id}/history`

Return the stored conversation history for one guest conversation.

### Path Parameters

| Name | Type | Description |
| --- | --- | --- |
| `conversation_id` | `string (UUID)` | Unique ID for the guest conversation. |

### Response Body

```json
{
  "conversation_id": "8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb",
  "messages": [
    {
      "role": "guest",
      "content": "Tell me about listing 101"
    },
    {
      "role": "assistant",
      "content": "Sea View Apartment in Cox's Bazar costs BDT 4,500 per night and includes WiFi, AC, and a kitchen."
    }
  ]
}
```

### Example

Request:

```http
GET /api/chat/8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb/history
```

Response:

```json
{
  "conversation_id": "8c6b2ed0-5b16-48ef-bedd-6a3ee2c8d5fb",
  "messages": [
    {
      "role": "guest",
      "content": "I need a room in Bandarban from 2026-07-01 to 2026-07-03 for 2 guests"
    },
    {
      "role": "assistant",
      "content": "I found 2 available properties in Bandarban: Hill View Cottage for BDT 4,200/night and Meghla Cabin for BDT 3,600/night."
    },
    {
      "role": "guest",
      "content": "Tell me about listing 204"
    },
    {
      "role": "assistant",
      "content": "Hill View Cottage in Bandarban costs BDT 4,200 per night and includes breakfast, WiFi, and mountain views."
    }
  ]
}
```

### Possible Error Responses

`404 Not Found`

```json
{
  "detail": "conversation not found"
}
```

`500 Internal Server Error`

```json
{
  "detail": "failed to load conversation history"
}
```
