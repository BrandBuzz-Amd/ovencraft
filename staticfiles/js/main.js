// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for navbar
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Add active class to nav links on scroll
    const sections = document.querySelectorAll('section[id]');
    
    function navHighlighter() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 100;
            const sectionId = current.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelector('.navbar-nav a[href*="' + sectionId + '"]')?.classList.add('active');
            } else {
                document.querySelector('.navbar-nav a[href*="' + sectionId + '"]')?.classList.remove('active');
            }
        });
    }
    
    window.addEventListener('scroll', navHighlighter);
});


// --- ADD THESE FUNCTIONS TO YOUR EXISTING main.js FILE ---

// Dynamic blog post loading functionality
function initDynamicBlogLoading() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            // Get current page and other parameters
            const currentPage = parseInt(this.getAttribute('data-page') || '1');
            const nextPage = currentPage + 1;
            const category = this.getAttribute('data-category') || '';
            
            // Show loading state
            const btnText = loadMoreBtn.querySelector('span');
            const spinner = loadMoreBtn.querySelector('.spinner-border');
            
            if (spinner) spinner.classList.remove('d-none');
            if (btnText) btnText.style.opacity = '0';
            
            // Load more posts via AJAX
            fetch(`/api/blog/posts?page=${nextPage}&limit=6${category ? '&category_id=' + category : ''}`)
                .then(response => response.json())
                .then(data => {
                    if (data.items && data.items.length > 0) {
                        // Append new posts to the container
                        const blogContainer = document.querySelector('.blog-posts-container');
                        
                        data.items.forEach(post => {
                            const postHtml = createBlogPostHtml(post);
                            blogContainer.insertAdjacentHTML('beforeend', postHtml);
                        });
                        
                        // Update button data attributes
                        loadMoreBtn.setAttribute('data-page', nextPage.toString());
                        
                        // Hide button if we've reached the last page
                        if (nextPage >= data.pages) {
                            loadMoreBtn.style.display = 'none';
                        }
                    } else {
                        // No more posts to load
                        loadMoreBtn.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error loading more posts:', error);
                    showAlert('Failed to load more posts. Please try again.', 'danger');
                })
                .finally(() => {
                    // Reset button state
                    if (spinner) spinner.classList.add('d-none');
                    if (btnText) btnText.style.opacity = '1';
                });
        });
    }
}

// Create HTML for a blog post
function createBlogPostHtml(post) {
    const formattedDate = new Date(post.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    return `
    <article class="blog-post">
        <div class="blog-post-image">
            <img src="${post.featured_image || 'https://via.placeholder.com/800x500'}" alt="${post.title}">
            ${post.categories.length > 0 ? 
                `<div class="post-category">${post.categories[0].name}</div>` : 
                ''}
        </div>
        <div class="blog-post-content">
            <div class="post-meta">
                <span class="post-date"><i class="bi bi-calendar3"></i> ${formattedDate}</span>
                <span class="post-author"><i class="bi bi-person"></i> ${post.author.username}</span>
            </div>
            <h2 class="post-title"><a href="/blog/${post.slug}">${post.title}</a></h2>
            <div class="post-excerpt">
                <p>${post.excerpt || post.content.substring(0, 150) + '...'}</p>
            </div>
            <a href="/blog/${post.slug}" class="read-more">Continue Reading <i class="bi bi-arrow-right"></i></a>
        </div>
    </article>
    `;
}

// Initialize comment form submission
function initCommentForm() {
    const commentForm = document.getElementById('comment-form');
    
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(commentForm);
            const commentData = {
                content: formData.get('content'),
                blog_id: formData.get('blog_id'),
                parent_id: formData.get('parent_id') || null
            };
            
            // Show loading state
            const submitBtn = commentForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...';
            
            // Submit comment via AJAX
            fetch('/api/blog/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(commentData)
            })
            .then(response => {
                if (!response.ok) {
                    // If response is not OK, try to get error message
                    return response.json().then(data => {
                        throw new Error(data.detail || 'Failed to submit comment');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Clear form and show success message
                commentForm.reset();
                
                // Show message about comment moderation
                showAlert('Your comment has been submitted and is awaiting moderation. Thank you!', 'success');
                
                // Reset any reply state
                const parentIdInput = commentForm.querySelector('input[name="parent_id"]');
                if (parentIdInput) parentIdInput.value = '';
                
                const replyInfo = document.getElementById('reply-info');
                if (replyInfo) replyInfo.style.display = 'none';
            })
            .catch(error => {
                console.error('Error submitting comment:', error);
                showAlert(error.message || 'Failed to submit comment. Please try again.', 'danger');
            })
            .finally(() => {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            });
        });
        
        // Handle reply functionality
        document.querySelectorAll('.comment-reply-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const commentId = this.getAttribute('data-comment-id');
                const commentAuthor = this.getAttribute('data-author');
                
                // Set parent ID in the hidden input
                const parentIdInput = commentForm.querySelector('input[name="parent_id"]');
                if (parentIdInput) parentIdInput.value = commentId;
                
                // Show reply info
                const replyInfo = document.getElementById('reply-info');
                if (replyInfo) {
                    replyInfo.style.display = 'block';
                    replyInfo.querySelector('.reply-to-name').textContent = commentAuthor;
                }
                
                // Scroll to comment form
                commentForm.scrollIntoView({ behavior: 'smooth' });
                
                // Focus on comment textarea
                commentForm.querySelector('textarea').focus();
            });
        });
        
        // Handle cancel reply
        const cancelReplyBtn = document.getElementById('cancel-reply');
        if (cancelReplyBtn) {
            cancelReplyBtn.addEventListener('click', function() {
                // Reset parent ID
                const parentIdInput = commentForm.querySelector('input[name="parent_id"]');
                if (parentIdInput) parentIdInput.value = '';
                
                // Hide reply info
                const replyInfo = document.getElementById('reply-info');
                if (replyInfo) replyInfo.style.display = 'none';
            });
        }
    }
}

// Initialize gallery filter functionality
function initGalleryFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    if (filterBtns.length && galleryItems.length) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                filterBtns.forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                btn.classList.add('active');
                
                const filterValue = btn.getAttribute('data-filter');
                
                galleryItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
}

// Initialize lightbox for gallery
function initLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxDescription = document.getElementById('lightbox-description');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxPrev = document.querySelector('.lightbox-prev');
    const lightboxNext = document.querySelector('.lightbox-next');
    let currentIndex = 0;
    let visibleItems = [];
    
    if (lightbox && lightboxImg) {
        // Open lightbox
        document.querySelectorAll('.gallery-zoom').forEach((item) => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get visible items
                visibleItems = Array.from(document.querySelectorAll('.gallery-item')).filter(
                    item => item.style.display !== 'none'
                );
                
                // Find current index
                const parentItem = this.closest('.gallery-item');
                currentIndex = visibleItems.indexOf(parentItem);
                
                // Get image data
                const imgSrc = this.getAttribute('data-img') || this.closest('.gallery-item').querySelector('img').src;
                const title = this.getAttribute('data-title') || this.closest('.gallery-item').querySelector('h3').textContent;
                const description = this.getAttribute('data-desc') || this.closest('.gallery-item').querySelector('p').textContent;
                
                // Set lightbox content
                lightboxImg.src = imgSrc;
                if (lightboxTitle) lightboxTitle.textContent = title;
                if (lightboxDescription) lightboxDescription.textContent = description;
                
                // Show lightbox
                lightbox.style.display = 'flex';
                setTimeout(() => {
                    lightbox.style.opacity = '1';
                }, 10);
                
                // Disable scrolling
                document.body.style.overflow = 'hidden';
            });
        });
        
        // Close lightbox
        if (lightboxClose) {
            lightboxClose.addEventListener('click', closeLightbox);
            
            // Close on background click
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox) {
                    closeLightbox();
                }
            });
        }
        
        // Navigate through lightbox
        if (lightboxNext) {
            lightboxNext.addEventListener('click', () => {
                currentIndex = (currentIndex + 1) % visibleItems.length;
                updateLightbox();
            });
        }
        
        if (lightboxPrev) {
            lightboxPrev.addEventListener('click', () => {
                currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
                updateLightbox();
            });
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (lightbox.style.display === 'flex') {
                if (e.key === 'Escape') {
                    closeLightbox();
                } else if (e.key === 'ArrowRight' && lightboxNext) {
                    lightboxNext.click();
                } else if (e.key === 'ArrowLeft' && lightboxPrev) {
                    lightboxPrev.click();
                }
            }
        });
    }
    
    function closeLightbox() {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            lightbox.style.display = 'none';
        }, 300);
        
        // Re-enable scrolling
        document.body.style.overflow = 'auto';
    }
    
    function updateLightbox() {
        const item = visibleItems[currentIndex];
        const img = item.querySelector('.gallery-img');
        const title = item.querySelector('.gallery-info h3')?.textContent;
        const description = item.querySelector('.gallery-info p')?.textContent;
        
        // Animate transition
        lightboxImg.style.opacity = '0';
        if (lightboxTitle) lightboxTitle.style.opacity = '0';
        if (lightboxDescription) lightboxDescription.style.opacity = '0';
        
        setTimeout(() => {
            lightboxImg.src = img.src;
            if (lightboxTitle) lightboxTitle.textContent = title;
            if (lightboxDescription) lightboxDescription.textContent = description;
            
            lightboxImg.style.opacity = '1';
            if (lightboxTitle) lightboxTitle.style.opacity = '1';
            if (lightboxDescription) lightboxDescription.style.opacity = '1';
        }, 300);
    }
}

// Initialize FAQ accordion functionality
function initFaqAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    const categoryBtns = document.querySelectorAll('.faq-category-btn');
    const faqItems = document.querySelectorAll('.faq-item');
    
    if (faqQuestions.length) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const faqItem = question.parentElement;
                const isActive = faqItem.classList.contains('active');
                
                // Close all open items
                document.querySelectorAll('.faq-item.active').forEach(item => {
                    item.classList.remove('active');
                    const icon = item.querySelector('.faq-icon i');
                    if (icon) {
                        icon.classList.remove('bi-dash');
                        icon.classList.add('bi-plus');
                    }
                });
                
                // Open the clicked item if it wasn't already open
                if (!isActive) {
                    faqItem.classList.add('active');
                    const icon = question.querySelector('.faq-icon i');
                    if (icon) {
                        icon.classList.remove('bi-plus');
                        icon.classList.add('bi-dash');
                    }
                }
            });
        });
    }
    
    // FAQ category filtering
    if (categoryBtns.length && faqItems.length) {
        categoryBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active button
                categoryBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const category = btn.getAttribute('data-category');
                
                // Filter items
                faqItems.forEach(item => {
                    if (category === 'all' || item.getAttribute('data-category') === category) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
}

// Show a message alert to the user
function showAlert(message, type = 'info') {
    // Create alert container if it doesn't exist
    let alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container';
        alertContainer.style.position = 'fixed';
        alertContainer.style.top = '20px';
        alertContainer.style.right = '20px';
        alertContainer.style.zIndex = '9999';
        alertContainer.style.maxWidth = '400px';
        document.body.appendChild(alertContainer);
    }
    
    // Create alert element
    const alertEl = document.createElement('div');
    alertEl.className = `alert alert-${type} alert-dismissible fade show`;
    alertEl.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Append alert to container
    alertContainer.appendChild(alertEl);
    
    // Initialize Bootstrap's alert dismiss functionality
    new bootstrap.Alert(alertEl);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertEl) {
            const bsAlert = bootstrap.Alert.getInstance(alertEl);
            if (bsAlert) bsAlert.close();
        }
    }, 5000);
}

// Add these function calls to your existing DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", function() {
    // Initialize existing functionality...
    
    // Initialize dynamic blog loading
    initDynamicBlogLoading();
    
    // Initialize comment form
    initCommentForm();
    
    // Initialize gallery filter
    initGalleryFilter();
    
    // Initialize lightbox
    initLightbox();
    
    // Initialize FAQ accordion
    initFaqAccordion();
});