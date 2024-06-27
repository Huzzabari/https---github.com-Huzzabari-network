document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.heartcontainer').forEach(function(like)
    {
      like.addEventListener('click', function(){      // when heart clicked on. function starts
        let user = like.getAttribute('data-user');     // gets the user info from the data attribute
        let post= like.getAttribute('data-post')        // gets the post info from the data attribute
        fetch('/update_likes/', {                       // uses the update likes view and does a post request
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({                            // makes the body 
              'likes': user, // likes key value pair is the user id clicking the like button
              'post': post   // post key value pair is the post id
          })
      })
      .then(response => response.json())
      .then(data => {
        let heart=data.heart;
        let like = document.querySelector(".heartcontainer i");
        if (heart) {
          like.className = 'fa-regular fa-heart';
      } else {
          like.className = 'fa-solid fa-heart';
      }
      document.querySelector(`#likes-count-${post}`).innerHTML = data.new_likes_count;  // update like count
      });
      });
    }); 
  });
  

//like and unlike post

//edit post


  