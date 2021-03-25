import moment from 'moment';

export const getStateIcon = (state) => {
    switch (state) {
        case "finished": return "mdi-stop";
        case "failed": return "mdi-close-circle";
        case "running": return "mdi-play";
        case "created": return "mdi-check";
        case 'stopping': return "mdi-motion-pause";
        case 'deleting': return "mdi-check";
        case 'published': return "mdi-television";
        default: return "mdi-cloud-refresh";
    }
}

export const getStateColor = (state) => {
    switch (state) {
        case "finished": return "success";
        case "failed": return "error";
        case "running": 
        case "published": 
            return "info";
        default: return "warning";
    }
}

export const copyToClipboard = (content) => {
    console.log(content);
    return false;
}

export const formatTime = (datetime) => {
    const t = moment(datetime.endsWith('Z') ? datetime : datetime + 'Z');
    const willHappen = t.fromNow();
    return `${t.format('LLL')} - ${willHappen}`;
}