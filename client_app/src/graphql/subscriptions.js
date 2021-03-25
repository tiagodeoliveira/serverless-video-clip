/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onUpdateTransmission = /* GraphQL */ `
  subscription OnUpdateTransmission {
    onUpdateTransmission {
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

export const onDeleteTransmission = /* GraphQL */ `
  subscription OnDeleteTransmission{
    onDeleteTransmission{
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

export const onUpdateClip = /* GraphQL */ `
  subscription OnUpdateClip{
    onUpdateClip{
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
export const onDeleteClip = /* GraphQL */ `
  subscription OnDeleteClip{
    onDeleteClip{
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
export const onCreateVote = /* GraphQL */ `
  subscription OnCreateVote(
    $id: String
    $clip_id: String
    $vote: String
    $created_at: String
    $user_id: String
  ) {
    onCreateVote(
      id: $id
      clip_id: $clip_id
      vote: $vote
      created_at: $created_at
      user_id: $user_id
    ) {
      id
      clip_id
      vote
      created_at
      user_id
    }
  }
`;
export const onDeleteVote = /* GraphQL */ `
  subscription OnDeleteVote(
    $id: String
    $clip_id: String
    $vote: String
    $created_at: String
    $user_id: String
  ) {
    onDeleteVote(
      id: $id
      clip_id: $clip_id
      vote: $vote
      created_at: $created_at
      user_id: $user_id
    ) {
      id
      clip_id
      vote
      created_at
      user_id
    }
  }
`;
