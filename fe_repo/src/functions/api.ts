import {v4 as uuidv4} from 'uuid';
import axios from "axios";
import __CURRENT_URI__ from '../../vite.config.ts';

const uri = __CURRENT_URI__ + ':5000'

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

export type LoginResponse = {
  user_id: string
}

export async function suggest(): Promise<QuestionResponse | null> {
  try {
    return axios.post<QuestionResponse>(uri + '/suggest/interiew_question',
      { user_id: getUserId() },
      { headers: { 'Content-Type': 'multipart/form-data' } })
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching response', error);
        return null;
      });
  } catch (error) {
    console.error('Error fetching the backend response', error);
    return null;
  }
}

export async function suggestJob(): Promise<QuestionResponse | null> {
  try {
    return axios.post<QuestionResponse>(uri + '/suggest/jobs',
      {user_id: getUserId()},
      {headers: {'Content-Type': 'multipart/form-data'}})
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching response', error);
        return null;
      });
  } catch (error) {
    console.error('Error fetching the backend response', error);
    return null;
  }
}

export async function sendMessage(message: string): Promise<QuestionResponse> {
  console.log("Sending message: " + message);
  try {
    return axios.post<QuestionResponse>(uri + '/chat',
      { question: message, user_id: getUserId() },
      { headers: { 'Content-Type': 'multipart/form-data' } })
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching response', error);
        return { response: "An error occurred, please try again later." };
      });
  } catch (error) {
    console.error('Error fetching the backend response', error);
    return { response: "An error occurred, please try again later." };
  }
}

export async function analyze(job_description: string): Promise<AnalzyeResponse | null> {
  console.log("analyzing", job_description);

  return axios.post<AnalzyeResponse>(uri + (job_description === '' ? '/resume_evaluate' : '/resume_evaluate_with_JD'),
    { jd_text: job_description, user_id: getUserId() },
    { headers: { 'Content-Type': 'multipart/form-data' } })
    .then(response => response.data)
    .catch(error => {
      console.error('Error fetching response', error);
      return null;
    });
}

export function uploadFile(file: File) {
  console.log("uploading file", file.name);
  axios.post(uri + '/upload', { file: file, user_id: getUserId() },
    { headers: { 'Content-Type': 'multipart/form-data' } })
    .then(() => {
      if (typeof window !== 'undefined') {
        alert("Resume uploaded successfully");
      }
      setHasResume(true);
    })
    .catch(error => {
      console.error('Error uploading resume', error);
      if (typeof window !== 'undefined') {
        alert("Cannot upload resume at this time, please try again later.");
      }
    });
}


export function hasUserId() {
  return localStorage.getItem('userId');
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

export function getHasResume() {
  if (typeof window === 'undefined') {
    return false;
  }
  return Boolean(localStorage.getItem('hasResume'));
}

export function setHasResume(hasResume: boolean) {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.setItem('hasResume', String(hasResume));
}

// login using google
export async function login(credential: string): Promise<string> {
  return axios.post<LoginResponse>(uri + '/login', { access_token: credential },
    { headers: { 'Content-Type': 'multipart/form-data' } })
    .then(resp => {
      alert("Login successful");
      return resp.data.user_id;
    })
    .catch(error => {
      console.error('Error fetching  response', error);
      return '';
    });
}
