import {v4 as uuidv4} from 'uuid';
import axios from "axios";

// TODO: Implement API functions

const uri = 'http://127.0.0.1:5000'

export type AnalzyeResponse = {
  analysis: {
    explanations: {
      [key: string]: {
        explanation: string,
        score: number
      }
    },
    scores: { [key: string]: number },
    weighted_total_score: number
  }
}

export type QuestionResponse = {
  response: string
}

export async function sendMessage(message: string): Promise<QuestionResponse> {
  console.log("Sending message: " + message);
  try {
    return axios.post<QuestionResponse>(uri + '/chat',
      {question: message, user_id: getUserId()},
      {headers: {'Content-Type': 'multipart/form-data'}})
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching response', error);
        return {response: "An error occurred, please try again later."};
      });
  } catch (error) {
    console.error('Error fetching the backend response', error);
    return {response: "An error occurred, please try again later."};
  }
}

export async function analyze(job_description: string): Promise<AnalzyeResponse | null> {
  console.log("analyzing", job_description);

  return axios.post<AnalzyeResponse>(uri + '/resume_evaluate',
    {job_description: job_description, user_id: getUserId()},
    {headers: {'Content-Type': 'multipart/form-data'}})
    .then(response => response.data)
    .catch(error => {
      console.error('Error fetching response', error);
      return null;
    });
}

export function uploadFile(file: File) {
  console.log("uploading file", file.name);
  axios.post(uri + '/upload', {file: file, user_id: getUserId()},
    {headers: {'Content-Type': 'multipart/form-data'}})
    .then(() => alert("Resume uploaded successfully"))
    .catch(error => console.error('Error fetching  response', error));
}


// user id
export function getUserId() {
  let uuid;
  if (typeof window !== 'undefined') {
    uuid = localStorage.getItem('userId') || uuidv4();
  } else {
    uuid = uuidv4();
  }
  setUserId(uuid);
  return uuid;
}

export function setUserId(userId: string) {
  if (!userId || typeof window === 'undefined') {
    return;
  }
  localStorage.setItem('userId', userId);
}

// login using google
export function login() {
  return getUserId();
}