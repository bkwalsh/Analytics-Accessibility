import { Octokit } from '@octokit/rest';
import { RequestError } from '@octokit/request-error';

export async function createRepoFile(
  token: string,
  owner: string,
  repo: string,
  path: string,
  content: string,
  message = 'Add file'
): Promise<string | null> {
  const octokit = new Octokit({ auth: token });
  const fileContentBase64 = btoa(unescape(encodeURIComponent(content)));

  let sha;
  try {
    const { data } = await octokit.repos.getContent({
      owner: owner,
      repo: repo,
      path: path
    });

    if (Array.isArray(data)) {
      alert('The path you provided is a directory.');
      return null;
    } else {
      sha = data.sha;
    }
  } catch (error) {
    if (error instanceof RequestError && error.status === 404) {
      // File does not exist so continue with creation.
    } else {
      console.log('Error getting file: ', error);
      return null;
    }
  }

  const file = {
    owner: owner,
    repo: repo,
    path: path,
    sha,
    message: message,
    content: fileContentBase64
  };

  if (sha) {
    file['sha'] = sha;
  }

  try {
    const response = await octokit.repos.createOrUpdateFileContents(file);
    return response.data?.content?.html_url || null;
  } catch (error) {
    console.error(error);
    return null;
  }
}
