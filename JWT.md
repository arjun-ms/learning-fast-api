
JWT stands for ***JSON Web Token***.

Imagine JWT as a **sealed envelope**:
- You send someone a **sealed envelope (token)** with your details (user ID, role).
- The receiver doesn’t need to ask you again who you are — they just **verify the seal (signature)**.
- If the seal’s broken or modified, they know it’s tampered.

It's a way to transmit information between parties as a JSON object. 
It's  used for **`authentication and data exchange`** in web development.

The JWT token is typically **stored** on the ***client side*.**

### Working
When a user logs in, the server generates a JWT containing user info, signs it, and sends it back to the client. The client can then include this token in future requests. The server verifies the token's signature, extracts the info, and processes the request.

==Traditional methods often involve **sessions and cookies**.==

When a user logs in, a session is created on the server, and a cookie is stored on the client's side. This can be effective, ***but it requires more server resources and can be complex to manage.*** 
## Features (Why does all developers prefer JWT token over cookies and sessions?)

1. **Compactness:**   They are **small in size**, making them **easy to transmit.**
2. **Stateless:**   The server **doesn’t need to remember you**—the JWT **carries everything** the server needs. The **client** stores the JWT (like in local storage or cookies).
3. **Self-contained:**   The token itself **contains all the information**, **reducing the need for constant database queries.** 
4. **Flexibility:**   Can be used for various purposes like **authentication** and **data exchange.**
5. **Security:**   Tokens can be **signed** to ensure their integrity, and some include encryption for added security.
6. **Reduced Database Queries:**   Since JWTs carry information, there's **less reliance on constant database queries**, making processes more efficient.

However, the choice depends on the specific needs of the application. Some scenarios might still benefit from traditional sessions and cookies.  

### Q: How secure are JWT tokens?

The security of JWTs **depends on proper implementation** and adherence to best practices by developers. Key aspects to ensure JWT security include:

1. **Secure Key Storage:**
    - Safely store secret keys used to sign JWTs. This prevents unauthorized tampering.
2. **Token Encryption:**
    - If sensitive information is stored in the JWT payload, encryption can be applied for an added layer of security.
3. **HTTPS Usage:**
    - Transmit JWTs over HTTPS to secure data during transport and prevent man-in-the-middle attacks.
4. **Short Expiration Times:**
    - Set short expiration times for tokens to limit their validity period, reducing the risk if a token is compromised.

### Why is it important to use HTTPS when working with JWTs?

HTTPS is crucial with JWTs because:

- JWTs are transmitted in headers or cookies, making them vulnerable to interception
- If a JWT is stolen via a non-encrypted connection, attackers can use it to impersonate users
- HTTPS encrypts the connection, protecting the token in transit
### Q: Can JWT tokens be revoked or invalidated?

Traditional JWTs are not easily revocable. One way to handle this is to set a relatively short expiration time and, if needed, use **token blacklisting** or implement **token refresh mechanisms.**

1. **Token Blacklisting:**
    - This is a method to address the lack of easy revocation in traditional JWTs.
    - When a token is blacklisted, the server maintains a list of revoked tokens.
    - Before processing a received token, the server checks if it's in the blacklist. If it is, access is denied.
    
2. **Token Refreshing:**
    - Tokens typically have an expiration time to enhance security.
    - Instead of requiring the user to log in again when a token expires, a refresh token is used.
    - When a token is about to expire, the user sends the refresh token to get a new access token without re-entering credentials.

### Q: Difference between a Access Token and Refresh Token

1. **Access Token Expiry:**
    - **Purpose:** The access token is used for regular authentication and authorization.
    - **Expiry Time:** Relatively short, typically minutes, to enhance security.
    - **Refresh:** When it expires, a new access token can be obtained using a refresh token.
	
2. **Refresh Token Expiry:**
    - **Purpose:** The refresh token is used to obtain a new access token without re-entering credentials.
    - **Expiry Time:** Longer compared to the access token, often days or weeks.
    - **Refresh:** When it expires, the user needs to re-authenticate to get a new refresh token.

### Q: What are the potential drawbacks or risks of using JWT?

Using JWTs comes with potential drawbacks and risks. Here are a few to be aware of:

1. **Token Theft:**
    - If an attacker gains access to a JWT, they can use it to impersonate the user. Protecting the token's secrecy is crucial.
2. **No Easy Revocation:**
    - Traditional JWTs are not easily revocable. Once issued, they remain valid until they expire. Strategies like short expiration times and token blacklisting help mitigate this.
3. **Size Limitations:**
    - As the information is carried within the token, large payloads can increase the size of each request, affecting performance.
4. **Statelessness Challenges:**
    - While statelessness is an advantage, it can be a challenge in scenarios where maintaining some state on the server is necessary.
5. **Complexity in Debugging:**
    - Debugging can be challenging as all necessary information is contained within the token. If an issue arises, it may require careful inspection.

### Q: Are there specific scenarios where sessions and cookies are still a better choice than JWT?

Sessions and cookies might be preferred in scenarios where stateful storage on the server is necessary, or when **simplicity and ease of implementation** are crucial.

---
---

## How would you implement a "logout" functionality with JWTs since they're stateless?

Since JWTs are stateless, you can implement logout through:

1. **Client-side approach**: Delete the token from client storage (localStorage, cookies)
2. **Token blacklist**: Maintain a server-side blacklist/database of invalidated tokens
3. **Short expiration times**: Use short-lived tokens with refresh token pattern
4. **Token versioning**: Add a token version to user record and increment on logout

## How would you handle token revocation before the expiration time?

1. **Token blacklist**:   Store revoked tokens in a database/cache
2. **Token versioning**:    Store a version number for each user, increment on revocation
3. **Redis/cache storage**:    Use fast in-memory storage to check against revoked tokens

## What security vulnerability could arise if you don't validate the incoming token properly?

Without proper validation:

- **Authentication bypass**: Attackers could forge or tamper with tokens
- **Expired token usage**: Users could continue using expired credentials
- **JWT algorithm confusion**: Attackers could change the algorithm header to exploit verification bugs
- **Missing signature verification**: Accepting a token without verifying its signature