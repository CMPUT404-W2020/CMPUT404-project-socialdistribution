//function to show comments
//Reference: https://stackoverflow.com/questions/29321494/show-input-field-only-if-a-specific-option-is-selected/29321711
//Author: https://stackoverflow.com/users/4721273/josephus87
function displayCommentsCheck(that) {
    if (document.getElementById(that).style.display == "block") {
        document.getElementById(that).style.display = "none";
    } else {
        document.getElementById(that).style.display = "block";
    }
}

function showDropdown(that) {
	document.getElementById(that).classList.toggle("show-dropdown");
}


function confirmDelete(post) {
	console.log(post);
	var yes = confirm("Are you sure you want to delete this post?\nThis action cannot be undone.");

	if (yes) {
		fetch('http://127.0.0.1:8000/delete/' + post, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
				},
			})
			.then((response)=> {
				if(response.status === 403){
					console.log("Forbidden: Cannot delete posts of other users");
				} else {
					console.log("Post deleted");
				}
				location.reload();
			});
	}
}


function simpleText() {
	var simple = document.getElementById("orange-button");
	simple.style.borderColor = "black";

	var markup = document.getElementById("blue-button");
	markup.style.borderColor = "lightgray";
}

function markupText() {
	var simple = document.getElementById("orange-button");
	simple.style.borderColor = "lightgray";

	var markup = document.getElementById("blue-button");
	markup.style.borderColor = "black";
}


