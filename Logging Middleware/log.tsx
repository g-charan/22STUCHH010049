// Defining the Params here
type params = {
  stack: string;
  level: string;
  pkg: string;
  message: string;
};

// Defining the end url
const TESTAPISERVER = "http://20.244.56.144/evaluation-service/logs";
const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW5ndXR0aTIyQGlmaGVpbmRpYS5vcmciLCJleHAiOjE3NTMyNTMxNTQsImlhdCI6MTc1MzI1MjI1NCwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjQ3Njg0YzA3LTY2NGUtNDVhYS04YjhjLWNhNDk2Mjk3YzkyMCIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImNoYXJhbiBndXR0aSIsInN1YiI6IjI0NmJhMjk1LTQ0ZWQtNDVlYi1hYjdhLTZlMGY4NTFiMjM0MCJ9LCJlbWFpbCI6ImNoYXJhbmd1dHRpMjJAaWZoZWluZGlhLm9yZyIsIm5hbWUiOiJjaGFyYW4gZ3V0dGkiLCJyb2xsTm8iOiIyMnN0dWNoaDAxMDA0OSIsImFjY2Vzc0NvZGUiOiJiQ3VDRlQiLCJjbGllbnRJRCI6IjI0NmJhMjk1LTQ0ZWQtNDVlYi1hYjdhLTZlMGY4NTFiMjM0MCIsImNsaWVudFNlY3JldCI6IkNRVFJ6WVJVS05jSEtwamgifQ.y_IOfyuBs1mMIfnQ6pui_RAQY38-3e6sNxDoT51JyVg";

// writing the function here
const Log = async ({ stack, level, pkg, message }: params) => {
  const requestPayload = {
    stack,
    level,
    package: pkg, //package cannot be used directly so it used like this
    message,
  };

  try {
    const response = await fetch(TESTAPISERVER, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // making sure the content type is consistent
      },
      body: JSON.stringify(requestPayload), // change the request payload to string
    });
    if (!response.ok) {
      throw new Error(`error:${response.status}`);
    }
  } catch (error) {
    console.error(`error: ${error}`);
  }
};
