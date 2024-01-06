"""
Design Facebook Comment System

Application Requirements:
---------------------------
Users should be able to comment on posts
Should be able to reply to comments
At most one level of nesting is allowed. If a user replies to a nested comment, the comment should appear below the previous comment
Users should be able to edit and delete their comments. The nesting should adjust on its own

Required Classes
--------------------
User Class
Comment Class
Post Class
"""

class User:
    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.posts = []
        self.comments = []
    
    def make_comment(self, comment, post):
        post.comments.append(comment)
        self.comments.append(comment)
        print(f"{comment.user.username} commented on post: {post.post} - {comment.text}")
    
    def make_post(self, post):
        self.posts.append(post)
        print(f" {self.username} posted - {post.post}")
    
    def reply_on_comments(self, comment, reply):
        comment.replies.append(reply)
        print(f"{reply.user.username} replied to {comment.user.username} on post: {comment.post.post} - {reply.text}")
    
    def edit_comment(self, comment, new_comment_text):
        if comment in self.comments:
            comment.text = new_comment_text
            print(f"Comment Updated Successfully - New Comment : {new_comment_text}")
            return
        print("No Comment Found!")         
    
    def delete_comment(self, comment, post):
        if comment in self.comments:
            self.comments.remove(comment)
            post.delete_comment(comment)
            print("Comment deleted Successfully!")
            return
        print("No comment Found!")

class Post:
    def __init__(self, post_id, post):
        self.post_id = post_id
        self.comments = []
        self.post = post
    
    def delete_comment(self, comment):
        if comment in self.comments:
            self.comments.remove(comment)

    def show_comments(self):
        print("\tPost\t\tComment\t\tUser")
        for comment in self.comments:
            print(f"{comment.post.post} - {comment.text} - {comment.user.username}")
    
class Comment:
    def __init__(self, post, user, text):
        self.post = post
        self.user = user
        self.text = text
        self.replies = []

if __name__ == '__main__':
   
   jai = User(1, "jai_panday", "jai@123", "jai@gmail.com")
   kishor = User(2, "Kishor9014", "kishor@123", "kishor@gmail.com")

   post1 = Post(1, "Hello World")
   post2 = Post(2, "India Lost WC2023")

   kishor.make_post(post2)
   comment_by_jai = Comment(post2, jai, "Was really heartbreaking!")
   jai.make_comment(comment_by_jai, post2)
   
   reply_by_kishor = Comment(post2, kishor, "Yes, it was!")
   kishor.reply_on_comments(comment_by_jai, reply_by_kishor)

   jai.delete_comment(comment_by_jai, post2)

   post2.show_comments()