// login to the server and return a JSON Web Token
export const login = async (username, password) => {
  const authRoute = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/auth/';
  let loginRoute = `${authRoute}login`;
  let loginResponse = await fetch(loginRoute, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  let authToken = (await loginResponse.json()).auth_token;
  return authToken;
};

export const getSiteActivity = async () => {
  const activityRoute = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/checkSites';
  let response = await fetch(activityRoute);
  let activity = await response.json();
  return activity;
}