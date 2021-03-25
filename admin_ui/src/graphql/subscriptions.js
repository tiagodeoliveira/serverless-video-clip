/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateTransmission = /* GraphQL */ `
  subscription OnCreateTransmission{
    onCreateTransmission{
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
export const onUpdateTransmission = /* GraphQL */ `
  subscription OnUpdateTransmission{
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


export const onCreateClip = /* GraphQL */ `
  subscription OnCreateClip{
    onCreateClip{
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
export const onUpdateClip = /* GraphQL */ `
  subscription OnUpdateClip{
    onUpdateClip {
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
  subscription OnCreateVote {
    onCreateVote {
      id
      clip_id
      vote
      created_at
      user_id
    }
  }
`;