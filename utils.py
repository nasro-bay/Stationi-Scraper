import os
from settings import COUNT

"""
Utility functions for OuedKniss API payloads and persistence.
"""

def get_payload_search(category_slug, page):
    """
    Constructs the GraphQL payload for searching announcements.
    
    Args:
        category_slug (str): The slug of the category to search.
        page (int): The page number to fetch.
        
    Returns:
        dict: The GraphQL request payload.
    """
    return {
        "operationName": "SearchQuery",
        "variables": {
            "q": None,
            "filter": {
                "categorySlug": category_slug,
                "origin": None,
                "connected": False,
                "delivery": None,
                "regionIds": [],
                "cityIds": [],
                "priceRange": [None, None],
                "exchange": None,
                "hasPictures": False,
                "hasPrice": False,
                "priceUnit": None,
                "fields": [],
                "page": page,
                "orderByField": {"field": "REFRESHED_AT"},
                "count": COUNT
            }
        },
        "query": """
        query SearchQuery($q: String, $filter: SearchFilterInput) {
            search(q: $q, filter: $filter) {
                announcements {
                    data {
                        id
                    }
                    paginatorInfo {
                        lastPage
                        hasMorePages
                    }
                }
            }
        }
        """
    }

def get_payload_post_all(ann_id):
    """
    Constructs a comprehensive GraphQL payload to fetch all details of an announcement.
    Includes technical specs, location, user info, and media.
    
    Args:
        ann_id (str): The ID of the announcement.
    """
    return {
        "operationName": "AnnouncementGet",
        "variables": {"id": str(ann_id)},
        "query": """
        query AnnouncementGet($id: ID!) {
            announcement: announcementDetails(id: $id) {
                id
                reference
                title
                slug
                description
                orderExternalUrl
                createdAt: refreshedAt
                price
                pricePreview
                oldPrice
                oldPricePreview
                priceType
                exchangeType
                priceUnit
                hasDelivery
                deliveryType
                hasPhone
                hasEmail
                quantity
                status
                street_name
                category {
                    id
                    slug
                    name
                    deliveryType
                    parentTree {
                        id
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                defaultMedia(size: ORIGINAL) {
                    mediaUrl
                    mimeType
                    thumbnail
                    __typename
                }
                medias(size: LARGE) {
                    mediaUrl
                    mimeType
                    thumbnail
                    __typename
                }
                categories {
                    id
                    name
                    slug
                    parentId
                    __typename
                }
                specs {
                    specification {
                        label
                        codename
                        type
                        __typename
                    }
                    value
                    valueText
                    __typename
                }
                user {
                    id
                    username
                    displayName
                    avatarUrl
                    __typename
                }
                isFromStore
                store {
                    id
                    name
                    slug
                    description
                    imageUrl
                    url
                    followerCount
                    viewAsStore
                    announcementsCount
                    status
                    locations {
                        location {
                            address
                            region {
                                slug
                                name
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    categories {
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                cities {
                    id
                    name
                    region {
                        id
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                isCommentEnabled
                noAdsense
                variants {
                    id
                    hash
                    specifications {
                        specification {
                            codename
                            label
                            __typename
                        }
                        valueText
                        value
                        mediaUrl
                        __typename
                    }
                    price
                    oldPrice
                    pricePreview
                    oldPricePreview
                    quantity
                    __typename
                }
                showAnalytics
                messengerLink
                __typename
            }
        }
        """
    }

def load_scraped_ids(filename):
    """
    Reads already processed announcement IDs from a persistence file.
    
    Args:
        filename (str): Path to the tracking file.
        
    Returns:
        set: A set of strings containing announcement IDs.
    """
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_scraped_id(filename, ann_id):
    """
    Persists a successfully scraped ID to the tracking file.
    
    Args:
        filename (str): Path to the tracking file.
        ann_id (str): The ID to save.
    """
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{ann_id}\n")

def get_payload_post_mini(ann_id):
    """
    Constructs a lightweight GraphQL payload for basic announcement details.
    
    Args:
        ann_id (str): The ID of the announcement.
    """
    return {
        "operationName": "AnnouncementGet",
        "variables": {"id": str(ann_id)},
        "query": """
        query AnnouncementGet($id: ID!) {
            announcement: announcementDetails(id: $id) {
                reference
                title
                description
                pricePreview
                priceUnit
                createdAt: refreshedAt
                specs {
                    specification {
                        label
                    }
                    valueText
                }
                cities {
                    name
                }
            }
        }
        """
    }