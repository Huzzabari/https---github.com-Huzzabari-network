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
      document.querySelector(`#likes-count-${post}`).innerHTML = data.new_likes_count;  // update like count based on post id.
      });
      });
    }); 

    // editing posts
   
    document.querySelectorAll('.edit').forEach(function(button)  //makes this change on each button
    {
      button.addEventListener('click', function(){      
        var postId=this.getAttribute('data-post_id');               //get the post id attribute
        fetch(`/edit/${postId}`)                                // fetch request started
        .then(response => response.json())
        .then(data => {
        textarea=document.createElement('textarea');            // create a text area and save it to a var
        textarea.id = 'myTextarea';                          // adding id, size, and placeholder data to text area var
        textarea.rows = 15;
        textarea.cols = 60;
        textarea.placeholder = data.form;
        document.querySelector(".text-area").append(textarea)         // I then append all this to the area I set in my html
        newButton=document.createElement('button');                 // I create a button and add id, data,etc. and then append it to the text area
        newButton.textContent='change';
        newButton.setAttribute('id', 'change-text');
        newButton.setAttribute('data-post-id', postId);
       document.querySelector(".text-area").append(newButton);
       textarea.scrollIntoView();                            // I cause the user to scroll to this new area
       newButton.addEventListener('click', function(){           // add the post click function to this button and then set a post fetch request
       let postId=newButton.getAttribute('data-post-id');           // save the post id data attribute 
       let text=document.querySelector('#myTextarea').value        // get the text in the text area box and save it 
       fetch(`/edit/${postId}`,{
        method: 'POST',
        headers:{
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({                                // send this info to the views.py
          'postId': postId,
          'text':text
        })
      })
        .then(response => response.json())
        .then(result => {                        
        //console.log(result.data.text);            // I was logging the result to see it in the console
        let postDiv=document.querySelector(`div[data-post-id="${postId}"]`)      // postdiv selected
       // console.log(postDiv);
        let pElement=postDiv.querySelector('p');                                // paragraphy selected
        //console.log(pElement);
        pElement.textContent=result.data.text;               // take the paragraph and replace it with the text I added from the textarea 
        let removeDiv=document.querySelector('#myTextarea');      // remove the text area
        removeDiv.remove();    // remove the div
        newButton.remove();    // remove the button
      })
    });
    });
     });
    }); 
    });



    
 
