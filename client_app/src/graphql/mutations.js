/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createTransmission = /* GraphQL */ `
  mutation CreateTransmission(
    $id: String
    $start: String
    $end: String
    $state: String
    $endpoints: String
    $name: String
    $description: String
    $created_at: String
    $stream_url: String
  ) {
    createTransmission(
      id: $id
      start: $start
      end: $end
      state: $state
      endpoints: $endpoints
      name: $name
      description: $description
      created_at: $created_at
      stream_url: $stream_url
    ) {
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
export const updateTransmission = /* GraphQL */ `
  mutation UpdateTransmission(
    $id: String
    $start: String
    $end: String
    $state: String
    $endpoints: String
    $name: String
    $description: String
    $created_at: String
    $stream_url: String
  ) {
    updateTransmission(
      id: $id
      start: $start
      end: $end
      state: $state
      endpoints: $endpoints
      name: $name
      description: $description
      created_at: $created_at
      stream_url: $stream_url
    ) {
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
export const deleteTransmission = /* GraphQL */ `
  mutation DeleteTransmission($id: String!) {
    deleteTransmission(id: $id) {
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
export const createClip = /* GraphQL */ `
  mutation CreateClip(
    $event_id: String
    $id: String
    $start: String
    $end: String
    $state: String
    $name: String
    $description: String
    $created_at: String
    $stream_url: String
  ) {
    createClip(
      event_id: $event_id
      id: $id
      start: $start
      end: $end
      state: $state
      name: $name
      description: $description
      created_at: $created_at
      stream_url: $stream_url
    ) {
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
export const updateClip = /* GraphQL */ `
  mutation UpdateClip(
    $event_id: String
    $id: String
    $start: String
    $end: String
    $state: String
    $name: String
    $description: String
    $created_at: String
    $stream_url: String
  ) {
    updateClip(
      event_id: $event_id
      id: $id
      start: $start
      end: $end
      state: $state
      name: $name
      description: $description
      created_at: $created_at
      stream_url: $stream_url
    ) {
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
export const deleteClip = /* GraphQL */ `
  mutation DeleteClip($id: String!) {
    deleteClip(id: $id) {
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
export const createVote = /* GraphQL */ `
  mutation CreateVote(
    $id: String
    $clip_id: String
    $vote: String
    $created_at: String
    $user_id: String
  ) {
    createVote(
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
export const updateVote = /* GraphQL */ `
  mutation UpdateVote(
    $id: String
    $clip_id: String
    $vote: String
    $created_at: String
    $user_id: String
  ) {
    updateVote(
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
export const deleteVote = /* GraphQL */ `
  mutation DeleteVote($id: String!) {
    deleteVote(id: $id) {
      id
      clip_id
      vote
      created_at
      user_id
    }
  }
`;
