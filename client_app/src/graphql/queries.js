/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getTransmission = /* GraphQL */ `
  query GetTransmission($id: String!) {
    getTransmission(id: $id) {
      id
      start
      end
      state
      endpoints
      name
      description
      created_at
      stream_url
    }
  }
`;
export const listTransmissions = /* GraphQL */ `
  query ListTransmissions(
    $filter: TableTransmissionsFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listTransmissions(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        start
        end
        state
        endpoints
        name
        description
        created_at
        stream_url
      }
      nextToken
    }
  }
`;
export const getClip = /* GraphQL */ `
  query GetClip($id: String!) {
    getClip(id: $id) {
      id
      event_id
      start
      end
      state
      name
      description
      created_at
      stream_url
    }
  }
`;
export const listClips = /* GraphQL */ `
  query ListClips(
    $filter: TableClipsFilterInput!
    $limit: Int
    $nextToken: String
  ) {
    listClips(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        event_id
        start
        end
        state
        name
        description
        created_at
        stream_url
      }
      nextToken
    }
  }
`;
export const getVote = /* GraphQL */ `
  query GetVote($id: String!) {
    getVote(id: $id) {
      id
      clip_id
      vote
      created_at
      user_id
    }
  }
`;
export const listVotes = /* GraphQL */ `
  query ListVotes(
    $filter: TableVotesFilterInput!
    $limit: Int
    $nextToken: String
  ) {
    listVotes(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        clip_id
        vote
        created_at
        user_id
      }
      nextToken
    }
  }
`;
