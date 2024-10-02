// TODO: Implement API functions

export function sendMessage(message: string) {
  // console.log("Sending message: " + message);
  try {
    // TODO: Implement sending message after api schema is provided
    // const response = await fetch('/api/chat', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ message: message })
    // });
    // const data = await response.json();

    const data = {
      result: "Message accepted: " + message
    }

    return data.result;
  } catch (error) {
    console.error('Error fetching the backend response', error);
    return "An error occurred, please try again later.";
  }
}

export function uploadFile(file: File) {
  console.log("uploading file", file.name);
  // const formData = new FormData();
  // formData.append('file', file);
  // fetch('/api/upload', {
  //   method: 'POST',
  //   body: formData,
  // }).then(response => response.json())
  //   .then(data => console.log('File upload success:', data))
  //   .catch(error => console.error('Error uploading file:', error));
}