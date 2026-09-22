# Notifications and unread state

Plainwire 2.5 keeps the activity inbox for things a person was asked to notice. Ordinary channel traffic stays on the channel.

## Inbox rows

A normal channel message does not insert an inbox row for every member. A mention still does. That includes a direct mention and, when the sender has the `mention_everyone` permission, `@everyone` and `@here`.

The realtime channel topic still carries the message for people who have that channel open.

## Opening a conversation

Opening a direct message, channel, or thread deletes the notification whose URL matches that destination. Marking a row seen used to leave it in the list. The URLs are `#/dm/:id`, `#/channel/:id`, and `#/t/:id`.

## Mention counts

The server rail and channel rows show mention counts. Channels inside a category use the same count as channels that are not categorized. A zero count is hidden.

## Direct messages

A direct-message transcript can show a "New messages" divider at the first unread entry.
