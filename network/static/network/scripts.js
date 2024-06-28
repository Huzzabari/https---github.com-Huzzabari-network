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
        let heart=data.heart;     // Let the true or false from the data saved to heart equal heart
        let hearticon = like.querySelector("i");       // hearticon is <i>
        if (heart) {     // If true make hearticon <i> class change to regular heart.
          hearticon.className = 'fa-regular fa-heart';
      } else {
          hearticon.className = 'fa-solid fa-heart';    // else solid heart
      }
      document.querySelector(`#likes-count-${post}`).innerHTML = data.new_likes_count;  // update like count
      });
      });
    }); 

    // Trying to edt posts
    document.querySelectorAll('.edit').forEach(function(button)
    {
      button.addEventListener('click', function(){      
        var postId=this.getAttribute('data-post_id');
        fetch(`/edit/${postId}`, {                       
          method: 'GET', 
       
        })
     });
    });
  });



  
  

//like and unlike post

//edit post


  