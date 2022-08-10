
**A Video Sharing and Streaming server made with Django.**


**Features**
- Users Management
  - three level/roles: normal user, admin, manager
- Proxy Server (for admin access)
- Ticketing System
  - users can send tickets to admins, and admins can send tickets to manager 
- iptables rules for basic DDoS Attack


# Structure
### Authentication and User Management ###
| path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | view list of videos | 
 | `profile/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | displaying username and staff status | 
 | `signup/` | POST | username, password | :heavy_check_mark: | :x: |  |  | 
 | `login/` | POST | username, password | :heavy_check_mark: | :x: |  |  | 
 | `admin_login/` | POST | username, password | :x: | :heavy_check_mark: |  |  | 
 | `admin_signup/` | POST | username, password | :x: | :heavy_check_mark: |  |  | 
 | `logout/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  |  | 
 | `strike_resolving/{username}/` | GET |  | :x: | :heavy_check_mark: | :heavy_check_mark: |  | 
 ### Videos ###
 | path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `upload/` | POST | title, video_file | :heavy_check_mark: | :x: |  | upload limit: 50MB | 
 | `video/{video_id}/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | watching video (with sockets) | 
 | `watch/{video_id}/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | watching video (html) | 
 | `watch/{video_id}/add_like/` | GET |  | :heavy_check_mark: | :x: |  |  | 
 | `watch/{video_id}/add_dislike/` | GET |  | :heavy_check_mark: | :x: |  |  | 
 | `watch/{video_id}/add_comment/` | POST | comment | :heavy_check_mark: | :x: |  |  | 
 | `video/add_lablel/` | POST | video_id | :x: | :heavy_check_mark: | :heavy_check_mark: | adding warning label to the video | 
 | `video/make_unavailable/` | POST | video_id | :x: | :heavy_check_mark: | :heavy_check_mark: | (user will get strike if +2 videos are removed) | 
### Ticketing System ###
 tickets statuses: `OPEN`, `PENDING`, `SOLVED`, `CLOSED`
 | path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `tickets/my/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | list of tickets created by user | 
 | `tickets/my/new/` | POST | title, text | :heavy_check_mark: | :heavy_check_mark: |  | create new ticket | 
 | `tickets/my/{ticket_id}/` | GET |  | :heavy_check_mark: | :heavy_check_mark: |  | display ticket information | 
 | `tickets/my/{ticket_id}/reply/` | POST | text | :heavy_check_mark: | :heavy_check_mark: |  | reply to a ticket | 
 | `tickets/users/` | GET |  | :x: | :heavy_check_mark: |  | list of tickets assigned to user | 
 | `tickets/users/all/` | GET |  | :x: | :heavy_check_mark: |  | list of unassigned tickets | 
 | `tickets/users/{ticket_id}/` | GET |  | :x: | :heavy_check_mark: |  | display ticket information | 
 | `tickets/users/{ticket_id}/assign/` | GET |  | :x: | :heavy_check_mark: | :heavy_check_mark: | assign ticket | 
 | `tickets/users/{ticket_id}/reply/` | GET |  | :x: | :heavy_check_mark: | :heavy_check_mark: | reply to a ticket | 
 | `tickets/users/{ticket_id}/close/` | GET |  | :x: | :heavy_check_mark: | :heavy_check_mark: | set ticket status to close | 
