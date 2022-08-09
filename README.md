
**A Video Sharing and Streaming server made with Django.**


**Features**
- Users Management
  - three level/roles: normal user, admin, manager
- Proxy Server (for admin access)
- Ticketing System
- iptables rules for basic DDoS Attack


# Structure
### Authentication and User Management ###
 | path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | view list of videos | 
 | `profile/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | displaying username and staff status | 
 | `signup/` | POST | username, password | :white_check_mark: | :white_large_square: | :white_large_square: |  | 
 | `login/` | POST | username, password | :white_check_mark: | :white_large_square: | :white_large_square: |  | 
 | `admin_login/` | POST | username, password | :white_large_square: | :white_check_mark: | :white_large_square: |  | 
 | `admin_signup/` | POST | username, password | :white_large_square: | :white_check_mark: | :white_large_square: |  | 
 | `logout/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: |  | 
 | `strike_resolving/{username}/` | GET |  | :white_large_square: | :white_check_mark: | :white_check_mark: |  | 
 
 ### Videos ###
 | path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `upload/` | POST | title, video_file | :white_check_mark: | :white_large_square: | :white_large_square: | upload limit: 50MB | 
 | `video/{video_id}/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | watching video (with sockets) | 
 | `watch/{video_id}/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | watching video (html) | 
 | `watch/{video_id}/add_like/` | GET |  | :white_check_mark: | :white_large_square: | :white_large_square: |  | 
 | `watch/{video_id}/add_dislike/` | GET |  | :white_check_mark: | :white_large_square: | :white_large_square: |  | 
 | `watch/{video_id}/add_comment/` | POST | comment | :white_check_mark: | :white_large_square: | :white_large_square: |  | 
 | `video/add_lablel/` | POST | video_id | :white_large_square: | :white_check_mark: | :white_check_mark: |  | 
 | `video/make_unavailable/` | POST | video_id | :white_large_square: | :white_check_mark: | :white_check_mark: |  | 
 
 ### Ticketing System ###
 | path | method | POST fields | user | admin | proxy | description | 
 | --- | :---: | --- | :---: | :---: | :---: | --- | 
 | `tickets/my/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | list of tickets created by user | 
 | `tickets/my/new/` | POST | title, text | :white_check_mark: | :white_check_mark: | :white_large_square: | create new ticket | 
 | `tickets/my/{ticket_id}/` | GET |  | :white_check_mark: | :white_check_mark: | :white_large_square: | display ticket information | 
 | `tickets/my/{ticket_id}/reply/` | POST | text | :white_check_mark: | :white_check_mark: | :white_large_square: | reply to a ticket | 
 | `tickets/users/` | GET |  | :white_large_square: | :white_check_mark: | :white_large_square: | list of tickets assigned to user | 
 | `tickets/users/all/` | GET |  | :white_large_square: | :white_check_mark: | :white_large_square: | list of unassigned tickets | 
 | `tickets/users/{ticket_id}/` | GET |  | :white_large_square: | :white_check_mark: | :white_large_square: | display ticket information | 
 | `tickets/users/{ticket_id}/assign/` | GET |  | :white_large_square: | :white_check_mark: | :white_check_mark: | assign ticket | 
 | `tickets/users/{ticket_id}/reply/` | GET |  | :white_large_square: | :white_check_mark: | :white_check_mark: | reply to a ticket | 
 | `tickets/users/{ticket_id}/close/` | GET |  | :white_large_square: | :white_check_mark: | :white_check_mark: | set ticket status to close | 
