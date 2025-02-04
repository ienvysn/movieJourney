  const modalTitle = document.getElementById("movieTitle");
  const modalDescription = document.getElementById("movieDescription");
  const modalrate=document.getElementById("movierate");
  const modalgenre=document.getElementById("moviegenre");
  const deleteForm = document.getElementById("deleteForm");
  const modal = document.getElementById("movieModal");
  const closeModalButton = document.querySelector(".close");
  const edit=document.getElementById("Edit_new");
  const completedForm = document.getElementById("completedForm");

  // Add event listeners to movie cards
document.querySelectorAll(".movie-card").forEach(card => {
  card.addEventListener("click", () => {
    // Get movie details from data attributes
    console.log("Movie card clicked");
    const m_id = card.getAttribute("data-movie-id");
    const name = card.getAttribute("data-name");
    const review = card.getAttribute("data-review");
    const rate = card.getAttribute("data-rating");
    const genre = card.getAttribute("data-genre");
    
    modalTitle.textContent = name;
    modalDescription.textContent = review;
    modalrate.textContent= rate;
    modalgenre.textContent=genre;
    console.log("Form action before setting:", edit.action);

    // Show modal
    modal.style.display = "flex";

     // Set delete form action dynamically
    deleteForm.action = `/delete_movie/${m_id}`;

    // Chnage wishlist to wtched
    
    edit.action=`/edit/${m_id}`;
    console.log("Form action after setting:", edit.action); 
    completedForm.action = `/completed/${m_id}`;
    

     //set edit form action dynamically 

     



  });
});

  // Close modal when clicking the close button
  closeModalButton.addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Close modal when clicking outside the modal content
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
