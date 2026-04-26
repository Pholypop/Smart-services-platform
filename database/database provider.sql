-- ========================================================
-- 1. ENUM TYPES
-- ========================================================
CREATE TYPE account_status AS ENUM ('PENDING', 'ACTIVE', 'SUSPENDED');
CREATE TYPE service_status AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');

-- ========================================================
-- 2.  Independent Tables
-- ========================================================

-- LOCATION
CREATE TABLE location (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(255),
    address VARCHAR(255),
    region VARCHAR(255)
);

-- SERVICE CATEGORY(أصناف الخدمات)
CREATE TABLE service_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- ========================================================
-- 3. جداول المزودين (Provider Related)
-- ========================================================

-- PROVIDER
CREATE TABLE provider (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE, -- مرتبط بجدول المستخدمين في نظام الـ Auth
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    bio TEXT,
    profile_image_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    experience_years INTEGER,
    rating_average DOUBLE PRECISION DEFAULT 0,
    trust_score DOUBLE PRECISION DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    status account_status DEFAULT 'PENDING',
    is_available BOOLEAN DEFAULT TRUE,
    location_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_provider_location
        FOREIGN KEY (location_id)
        REFERENCES location(id)
        ON DELETE SET NULL
);

-- ✅ الجدول الوسيط (The Pivot Table)
--fix problem ( sign up : category)
CREATE TABLE provider_category (
    provider_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    PRIMARY KEY (provider_id, category_id),
    
    CONSTRAINT fk_pc_provider 
        FOREIGN KEY (provider_id) 
        REFERENCES provider(id) 
        ON DELETE CASCADE,
        
    CONSTRAINT fk_pc_category 
        FOREIGN KEY (category_id) 
        REFERENCES service_category(id) 
        ON DELETE CASCADE
);

-- ========================================================
-- 4. Service Related
-- ========================================================

-- SERVICE
CREATE TABLE service (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL, -- 
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status service_status DEFAULT 'DRAFT',
    price DOUBLE PRECISION,
    currency VARCHAR(10) DEFAULT 'DZD',
    image_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    rating_average DOUBLE PRECISION DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    publication_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_service_provider
        FOREIGN KEY (provider_id)
        REFERENCES provider(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_service_category
        FOREIGN KEY (category_id)
        REFERENCES service_category(id)
);

-- TASK
CREATE TABLE task (
    id BIGSERIAL PRIMARY KEY,
    service_id BIGINT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    duration INTEGER, 
    price DOUBLE PRECISION,
    mandatory BOOLEAN DEFAULT TRUE,
    image_url TEXT,

    CONSTRAINT fk_task_service
        FOREIGN KEY (service_id)
        REFERENCES service(id)
        ON DELETE CASCADE
);

-- PORTFOLIO IMAGES

CREATE TABLE portfolio_image (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL,
    image_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_portfolio_provider
        FOREIGN KEY (provider_id)
        REFERENCES provider(id)
        ON DELETE CASCADE
);

-- ========================================================
-- 5. INDEXES 
-- ========================================================
CREATE INDEX idx_provider_user ON provider(user_id);
CREATE INDEX idx_provider_category_pivot ON provider_category(category_id);
CREATE INDEX idx_service_provider ON service(provider_id);
CREATE INDEX idx_service_category ON service(category_id);
CREATE INDEX idx_task_service ON task(service_id);
CREATE INDEX idx_portfolio_provider ON portfolio_image(provider_id);