USE wave_friend2;

INSERT INTO users (name, email, password, birthdate, gender, bio) VALUES
('Alice', 'alice@example.com', 'hashed_password1', '1995-06-15', 'woman', 'Loves traveling and coding.'),
('Bob', 'bob@example.com', 'hashed_password2', '1992-03-22', 'man', 'Guitarist and coffee enthusiast.'),
('Charlie', 'charlie@example.com', 'hashed_password3', '1998-11-30', 'nonbinary', 'Aspiring writer and nature lover.'),
('David', 'david@example.com', 'hashed_password4', '1990-07-08', 'man', 'Enjoys hiking and photography.'),
('Eve', 'eve@example.com', 'hashed_password5', '1996-12-25', 'other', 'Tech geek and sci-fi fan.');

INSERT INTO photos (user_id, uri) VALUES
(1, 'https://wavefriend.com/photos/alice1.jpg'),
(1, 'https://wavefriend.com/photos/alice2.jpg'),
(1, 'https://wavefriend.com/photos/alice3.jpg'),
(2, 'https://wavefriend.com/photos/bob1.jpg'),
(2, 'https://wavefriend.com/photos/bob2.jpg'),
(3, 'https://wavefriend.com/photos/charlie1.jpg'),
(3, 'https://wavefriend.com/photos/charlie2.jpg'),
(3, 'https://wavefriend.com/photos/charlie3.jpg'),
(3, 'https://wavefriend.com/photos/charlie4.jpg'),
(4, 'https://wavefriend.com/photos/david1.jpg'),
(5, 'https://wavefriend.com/photos/eve1.jpg'),
(5, 'https://wavefriend.com/photos/eve2.jpg');

INSERT INTO waves (sender_id, receiver_id, wave_time) VALUES
(1, 3, '2025-03-23 10:15:00'),
(3, 1, '2025-03-23 10:16:00'),
(3, 4, '2025-03-23 11:00:00'),
(4, 5, '2025-03-23 11:02:00'),
(5, 1, '2025-03-23 12:30:00'),
(2, 5, '2025-03-23 12:31:00'),
(2, 3, '2025-03-23 13:45:00'),
(5, 4, '2025-03-23 14:31:00'),
(3, 2, '2025-03-23 14:46:00');

INSERT INTO bonds (user1_id, user2_id, bonded_at) VALUES
(1, 3, '2025-03-23 10:16:00'),
(4, 5, '2025-03-23 14:31:00'),
(2, 3, '2025-03-23 14:46:00');

INSERT INTO messages (bond_id, sender_id, text, sent_at, is_read) VALUES
(1, 1, 'Hey, nice to connect!', '2025-03-23 10:20:00', TRUE),
(1, 3, 'Yeah! Happy to meet you!', '2025-03-23 10:22:00', TRUE),
(1, 1, 'So what do you usually do for fun?', '2025-03-23 10:25:00', TRUE),
(1, 3, 'I like hiking and coding. You?', '2025-03-23 10:27:00', TRUE),
(1, 1, 'Oh nice! I love coding too. What projects are you working on?', '2025-03-23 12:30:00', TRUE),
(1, 3, 'I’m building a small app for tracking habits.', '2025-03-23 12:32:00', TRUE),
(1, 1, 'That sounds useful! Using any specific tech stack?', '2025-03-23 13:34:00', TRUE),
(1, 3, 'Yeah, mainly React for frontend and Laravel for backend.', '2025-03-23 13:36:00', TRUE),
(1, 1, 'Laravel? Nice choice. I’ve been learning it recently.', '2025-03-23 13:38:00', TRUE),
(1, 3, 'Yeah, it’s pretty nice. What about you? Working on anything cool?', '2025-03-23 13:40:00', TRUE),
(1, 1, 'I’m playing around with some AI projects in Python.', '2025-03-23 10:42:00', TRUE),
(1, 3, 'That’s awesome! Ever tried integrating AI with web apps?', '2025-03-23 13:45:00', TRUE),
(2, 4, 'Hello! How are you?', '2025-03-23 14:35:00', TRUE),
(2, 5, 'Hey! Doing well, thanks!', '2025-03-23 14:37:00', FALSE),
(1, 1, 'Not yet, but I’d love to. Maybe we can collaborate on something?', '2025-03-23 14:47:00', TRUE),
(1, 3, 'That would be cool! Let’s discuss ideas sometime.', '2025-03-23 14:50:00', FALSE),
(3, 2, 'Hey, finally bonded!', '2025-03-23 14:50:30', TRUE),
(3, 3, 'Yes! Looking forward to chatting!', '2025-03-23 14:52:00', TRUE);

