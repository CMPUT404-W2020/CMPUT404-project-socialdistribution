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

//used to show drop down information on the notification page
//will switch between showArrow element and hideArrow element
function displayNotifications(content,hideArrow, showArrow) {
  if (document.getElementById(content).style.display == "block") {
    document.getElementById(content).style.display = "none";
  } else {
    document.getElementById(content).style.display = "block";
  }
  document.getElementById(hideArrow).style.display = "none";
  document.getElementById(showArrow).style.display = "inline-block";
}

function showDropdown(that) {
  document.getElementById(that).classList.toggle("show-dropdown");
}

function confirmDelete(post) {
  const origin = window.location.origin;
  console.log(origin);
  console.log(post);
  var yes = confirm(
    "Are you sure you want to delete this post?\nThis action cannot be undone."
  );

  const data = {
    target_post: post
  };

  if (yes) {
    fetch(origin + "/deletepost", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      alert(
        `Post deleted!`
        );
        location.reload();
      })
      .catch(function(error) {
        alert(
          "Couldn't delete post.\nPlease try again later."
          );
      });
  }
}

function confirmDeleteUser(author) {
  var yes = confirm(
    "Verify user?"
  );

  if (yes) {
    const origin = window.location.origin;
    const data = {
      target_author: author
    };
    fetch(origin + "/deleteuser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      if (!response.ok){
        throw Error(response.statusText)
      }
      return response
    })
    .then(function(response) {
      alert(
        `User deleted!`
        );
        location.reload();
      })
      .catch(function(error) {
        alert(
          "Couldn't delete user.\nPlease try again later."
          );
      });
    }
}

function confirmVerify(author) {
  var yes = confirm(
    "Verify user?"
  );

  if (yes) {
    const origin = window.location.origin;
    const data = {
      target_author: author
    };
    fetch(origin + "/verifyuser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      if (!response.ok){
        throw Error(response.statusText)
      }
      return response
    })
    .then(function(response) {
      alert(
        `User verified!`
        );
        location.reload();
      })
      .catch(function(error) {
        alert(
          "Couldn't verify user.\nPlease try again later."
          );
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

function makeItAList(val) {
  // Use regex to replace weird characters
  // and anything that isn't strictly the author's name
  val = val.replace(/&lt;/g, "");
  val = val.replace(/&gt;/g, "");
  val = val.replace(/Author: /g, "");

  // It may look like a list, but it's still a string
  val = val.replace(/\[/g, "");
  val = val.replace(/\]/g, "");
  val = val.replace(/, /g, ",");
  val = val.split(","); // now it's a list

  if (val == "") {
    return [];
  }

  return val;
}

function makeItADict(val) {
  // This function turns a mess of a returned dictionary
  // into a once-again legible dictionary
  val = val.replace(/\[\{/g, "");
  val = val.replace(/\}\]/g, "");
  val = val.replace(/&#x27;/g, "");

  val = val.split("}, {");

  ret_val = [];
  for (let v of val) {
    var entry = {};
    v = v.split(", ");
    for (let x of v) {
      x = x.split(": ");
      entry[x[0]] = x[1];
    }
    ret_val.push(entry);
  }

  return ret_val;
}

function createButtonId(name) {
  return "circle-button-" + name.replace(/ /g, "-") + "";
}

function createStatusId(name) {
  return "status-" + name.replace(/ /g, "-") + "";
}

function sendRequest(author) {
  const origin = window.location.origin;

  const data = {
    target_author: author
  };
  fetch(origin + "/friendrequest", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(function(response) {
    if (!response.ok){
      throw Error(response.statusText)
    }
    return response
  })
  .then(function(response) {
    alert(
      `Friend request successfully sent to ${author}.\nYou are now following ${author}.`
      );
      location.reload();
    })
    .catch(function(error) {
      alert(
        "Friend request could not be sent at this time.\nPlease try again later."
        );
    });
}

function rejectRequest(author) {
  const origin = window.location.origin;

  const data = {
    target_author: author
  };
  fetch(origin + "/rejectrequest", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(function(response) {
    if (!response.ok){
      throw Error(response.statusText)
    }
    return response
  })
  .then(function(response) {
    alert(
      `Friend request rejected.\nYou can still follow ${author} by searching for them.`
      );
      location.reload();
    })
    .catch(function(error) {
      alert(
        "Your request not be processed at this time.\nPlease try again later."
        );
    });
}

function removeFriend(author) {
  var yes = confirm(
    "Would you like to remove this friend?\nThis author can still follow your posts even if you remove them as a friend."
  );

  if (yes) {
    const origin = window.location.origin;
    const data = {
      target_author: author
    };
    fetch(origin + "/unfollow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      if (!response.ok){
        throw Error(response.statusText)
      }
      return response
    })
      .then(function(data) {
        alert(
          `You have successfully removed them as a friend.\n They can still see your public posts.`
        );
        location.reload();
      })
      .catch(function(data) {
        alert(
          "This friend could not be removed at this time.\nPlease try again later."
        );
      });
    location.reload();

  }
}

function unfollow(author) {
  var yes = confirm("Would you like to unfollow this author?");

  if (yes) {
    const origin = window.location.origin;
    const data = {
      target_author: author
    };
    fetch(origin + "/unfollow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      if (!response.ok){
        throw Error(response.statusText)
      }
      return response
    })
    .then(function(response) {
      alert(`You have successfully unfollowed this user.`);
      location.reload();
    })
    .catch(function(error) {
      alert(
        "This author could not be unfollowed at this time.\nPlease try again later."
      );
    });
    location.reload();

  }
}

function updateInnerHTML(name, status) {
  // This function is not currently used 'cause it's hard to change the
  // onclick attribute of a button. However, this function does successfully
  // change the status message and button icon when the button is pressed.
  // I'm thinking a simple page reload might be easier though

  // name is the author upon which to perform the action
  // status is the action to be performed

  var btn_id = createButtonId(name);
  var status_id = createStatusId(name);

  if (status == "follow") {
    document.getElementById(btn_id).innerText = "-";

    var status = document.getElementById(status_id).innerText;
    if (status.toUpperCase() == "FOLLOWS YOU") {
      document.getElementById(status_id).innerText = "Friends";
      // new action: unfriend
      // need uuid for this
      document.getElementById(btn_id).innerText = () => {};
    } else {
      document.getElementById(status_id).innerText = "Following";
      // new action: unfollow
      // need uuid for this
      document.getElementById(btn_id).innerText = () => {};
    }
  }

  if (status == "unfriend") {
    document.getElementById(btn_id).innerText = "+";
    document.getElementById(status_id).innerText = "Follows You";
    // new action: friend
    // only need the name to send a friend request!
    document
      .getElementById(btn_id)
      .setAttribute("onclick", `"sendRequest('${author}')"`);
  }

  if (status == "unfollow") {
    document.getElementById(btn_id).innerText = "+";
    document.getElementById(status_id).innerText = "";
    // new action: follow
    // only need a name to send a follow!
    document
      .getElementById(btn_id)
      .setAttribute("onclick", `"sendRequest('${author}')"`);
  }
}

